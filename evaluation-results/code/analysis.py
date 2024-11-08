import os

# Specify the directory you want to iterate through
root_directory = "./percentages"

for root, dirs, filenames in os.walk(root_directory):
    # print(f"Currently in directory: {root}")
    # For the subdirectories with files (assumption it's a 1 level tree)
    if len(filenames) > 0:
        # print("\tProcessing files...")
        model = root.split("/")[-1].lower()
        with open(f"summary-stats-{model}.csv", "w") as out:
            header = ["file", "comp", "matches", "percent"]
            headerline = ",".join(header)
            out.write(f"{headerline}\n")
            counter = 0
            row_counter = 0
            accum = [0,0,0,0]
            for filename in filenames:
                if "summary_results" in filename:
                    continue
                filename = os.path.join(root,filename)
                with open(filename) as f:
                    lines = [line.strip() for line in f.readlines() if len(line) > 1]
                    lines = [line.split(": ")[1] for line in lines]
                    data, comp, matches, percent, *tail = lines

                    if matches == "0":
                        counter += 1

                    accum[0] += int(matches)
                    accum[1] += int(comp)
                    accum[2] += int(matches) / int(comp)
                    if matches != "0":
                        accum[3] += int(comp)

                    row_tokens = lines[:4]
                    row_line = ",".join(row_tokens)
                    out.write(f"{row_line}\n")
                    row_counter += 1
            # print(filename)
            # print(f"Rows: {row_counter}")
            # print(f"Total Coverage: {accum[0]/accum[1]}")
            # print(f"Average Coverage: {accum[2]/row_counter}")
            nz_rows = row_counter - counter
            # print(f"NZ_Rows: {nz_rows}")
            # print(f"Total Coverage: {accum[0]/accum[3]}")
            # print(f"Average Coverage: {accum[2]/nz_rows}")
            # print(f"There were {counter} failures to extract any triples.")
            covs = [accum[0]/accum[1], accum[2]/row_counter, accum[0]/accum[3], accum[2]/nz_rows]
            covs = [cov * 100 for cov in covs]
            covs = [str(cov)[:5] for cov in covs]
            rtc, rac, nztc, nzac = covs

            model = root.split("/")[-1].replace("_","\\_")

            cells = [model, rtc, rac, counter, nztc, nzac ]
            cells = [str(cell) for cell in cells]
            cell_line = " & ".join(cells)
            print(f"{cell_line}\\\\\\hline")
    # print("-" * 40)