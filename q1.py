import json
import csv 


# open and load input file for reading
def load_input(fname):
    with open(fname) as infile:
        data = json.load(infile)
    return data

def get_most_common_player(data):
    player_count = {}

    for snapshot in data["snapshots"]:
        for row in snapshot:
            player_value = (row['player'], row['contract'])
            player_count[player_value] = player_count.get(player_value, 0) + 1

    most_common_player = max(player_count, key=player_count.get)

    return most_common_player[0]

def sort_by_paid(data, player_id):
    only_max = []
    for snapshot in data["snapshots"]:
        print("\n") 
        snapshot.sort(key=lambda player: (( player["paid"], player["player"] )))

        for row in snapshot:
            if (row["player"] == player_id):
                only_max.append(row)

    only_max.sort(key=lambda x: x["paid"] )

    return only_max

def map_roster_days(only_max, data, new_data):
    for om in only_max:
        for snapshot in data["snapshots"]:
            if (om in snapshot):
                new_data["snapshots"].append(snapshot)

    return new_data

def write_to_csv(output_file, data, headers):
    with open(output_file, mode="w", newline="") as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(headers)

        for snap in data:
            selected_values = [snap[key] for key in headers] 
            csv_writer.writerow(selected_values)

def add_roster_day_to_player(data):
    for idx, snapshots in enumerate(data["snapshots"]):
        snapshots.sort(key=lambda player:player["player"] )

        for snapshot in snapshots:
            snapshot["roster_day"] = idx

def create_one_big_list(data):
    only_snaps = []
    for snapshots in data["snapshots"]:
        for snapshot in snapshots:
            only_snaps.append(snapshot)
    

    only_snaps.sort(key=lambda x:x["player"])

    return only_snaps

def main():
    # input and output file names
    input_file = "q1_snapshots.json"
    output_file = "q1_output.csv"

    data = load_input(input_file)

    headers = ["player", "contract", "roster_day"]

    player_id = get_most_common_player(data)

    snapshot_of_max_player = sort_by_paid(data, player_id)

    ordered_snapshots = {"snapshots": []}

    new_data = map_roster_days(snapshot_of_max_player, data, ordered_snapshots)
  
    add_roster_day_to_player(new_data)

    list_to_write = create_one_big_list(ordered_snapshots)

    write_to_csv(output_file, list_to_write, headers)



if __name__ == "__main__":
    main()

