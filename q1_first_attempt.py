import json
import csv 


# open and load input file for reading
def load_input(fname):
    with open(fname) as infile:
        data = json.load(infile)
    return data

def process_snapshot_data(data):
    # list to store intermediate data of player, contract and roster day
    unsorted_data = []

    # enumerate through all snapshots data
    for idx, snapshots in enumerate(data["snapshots"]):
        # for each snapshot per day
        for snapshot in snapshots:
            # add which day of the season we're on
            snapshot["roster_day"] = idx
            # add row data to our intermediary list
            unsorted_data.append(snapshot)
    return unsorted_data

def sort_player_data(unsorted_data):
    # using the built in sorted method, we sort the unsorted data and use the first
    # column as what we're sorting by
    sorted_data = sorted(unsorted_data, key=lambda row: row["player"])
    return sorted_data

def write_to_csv(sorted_data, output_file, headers):
    # open our output csv file
    with open(output_file, mode="w", newline="") as outfile:
        csv_writer = csv.writer(outfile)
        # first write the header rows declared on line 9
        csv_writer.writerow(headers)

        # for each row in our newly sorted data
        for row in sorted_data:
            # we're grabbing only selected vals, we don't want the paid value in our file data
            selected_values = [row[key] for key in headers] 
            # write to csv
            csv_writer.writerow(selected_values)

def main():
    # input and output file names
    input_file = "q1_snapshots.json"
    output_file = "q1_output.csv"

    # hardcoded header rows for csv output file
    headers = ["player", "contract", "roster_day"]
   
    # error handler for loading input file
    try:
        data = load_input(input_file)
    except Exception as e:
        print(f"Oops! An error occured while loading the input file. Error: {e}")
        return

    # error handler for processing player adta
    try:
        unsorted_data = process_snapshot_data(data)
        sorted_data = sort_player_data(unsorted_data)
    except Exception as e:
        print(f"Oops! An error occured while processing player data. Error: {e}")
        return
    
    # error handler for writing to output file
    try:
        write_to_csv(sorted_data, output_file, headers)
    except Exception as e:
        print(f"Oops! An error occured while writing data. Error: {e}")
        return

    print("Complete! Please open " + output_file + " to view processed data.")


if __name__ == "__main__":
    main()