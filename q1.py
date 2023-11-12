import json
import csv 

# open and load input file for reading
def load_input(fname):
    with open(fname) as infile:
        data = json.load(infile)
    return data

def get_player_id_data(data):
    player_count = {}
    all_player_ids = set()

    for snapshot in data["snapshots"]:
        for row in snapshot:
            all_player_ids.add(row['player'])
            player_value = (row['player'], row['contract'])
            player_count[player_value] = player_count.get(player_value, 0) + 1

    most_common_player = max(player_count, key=player_count.get)
    return most_common_player[0], all_player_ids

def sort_by_paid(data, player_id):
    only_max = []
    for snapshot in data["snapshots"]:
        snapshot.sort(key=lambda player: (( player["paid"], player["player"] )))

        for row in snapshot:
            if (row["player"] == player_id):
                only_max.append(row)

    only_max.sort(key=lambda x: x["paid"] )

    return only_max

def determine_snapshot_order(only_max, data, new_data):
    for idx, om in enumerate(only_max):
        for snapshot in data["snapshots"]:
            if (om in snapshot):
                for row in snapshot:
                    row["day"] = idx
                new_data["snapshots"].append(snapshot)

    return new_data

def write_to_csv(output_file, data, headers):
    with open(output_file, mode="w", newline="") as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(headers)

        for snap in data:
            if "roster_day" in snap:
                selected_values = [snap[key] for key in headers] 
                csv_writer.writerow(selected_values)

def create_one_big_list(data):
    # print(data)
    only_snaps = []
    for snapshots in data["snapshots"]:
        for snapshot in snapshots:
           only_snaps.append(snapshot)    
    

    only_snaps.sort(key=lambda x:x["player"])
    return only_snaps

def get_roster_days_for_player(data):
    for i in range(1, len(data)):
        prev_day = data[i-1]
        curr_day = data[i]
        curr_paid_amnt = curr_day["paid"]
        prev_paid_amnt = prev_day["paid"]

        if (prev_paid_amnt == 0):
            prev_day["roster_day"] = 0
        
        elif (curr_paid_amnt > prev_paid_amnt):
            if ("roster_day" not in prev_day):
                prev_day["roster_day"] = prev_day["day"]
            else:
                prev_day["roster_day"] = i-1
        elif (curr_paid_amnt == prev_paid_amnt):
            continue 
    
    return data

def get_players_by_id(all_player_ids, data):
    players_by_id = []
    for id in all_player_ids:
        new_list = []
        for item in data:
            if (item['player'] == id):
                new_list.append(item)
        players_by_id.append(new_list)
    
    return players_by_id

def get_all_players_and_roster_days(players_by_id, new_data):
    for item in players_by_id:
        new_snaps = get_roster_days_for_player(item)
        new_data["snapshots"].append(new_snaps)

    return new_data


def main():
    input_file = "q1_snapshots.json"
    output_file = "q1_output.csv"

    data = load_input(input_file)

    headers = ["player", "contract", "roster_day"]

    player_id, all_player_ids = get_player_id_data(data)
    snapshot_of_max_player = sort_by_paid(data, player_id)

    ordered_snapshots = {"snapshots": []}

    new_data = determine_snapshot_order(snapshot_of_max_player, data, ordered_snapshots)
    new_data_as_list = create_one_big_list(new_data)
    players_by_id = get_players_by_id(all_player_ids, new_data_as_list)

    ordered_snapshots_with_roster_day = {"snapshots": [] }

    to_write = get_all_players_and_roster_days(players_by_id, ordered_snapshots_with_roster_day)

    to_write_csv = create_one_big_list(to_write)
    write_to_csv(output_file, to_write_csv, headers)
    

if __name__ == "__main__":
    main()

