import requests , sqlite3 , json , os.path

Hacker01Url = "https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/hackerone.json"

# Database Management
class DBM:
    def InitDB(file):
        conn = sqlite3.connect(file) 
        query = conn.cursor()
        query.execute('CREATE TABLE Programs (name VARCHAR(255),handle VARCHAR(255),submission_state BOOLEAN,offers_bounties BOOLEAN,UNIQUE(name));')
        query.execute('CREATE TABLE Assets (name VARCHAR(255), asset_type VARCHAR(255), asset_identifier VARCHAR(255), eligible_for_bounty BOOLEAN, instruction VARCHAR(1200),UNIQUE(asset_identifier));')
        conn.commit()
        conn.close()



    def InitData(file , name , handle , submission_state , offers_bounties , asset_type ,asset_identifier , eligible_for_bounty , instruction):
        conn = sqlite3.connect(file) 
        query = conn.cursor()
        query.execute("INSERT OR IGNORE INTO Programs (name, handle, submission_state, offers_bounties) VALUES (?, ?, ?, ?);", (name, handle, submission_state, offers_bounties))
        query.execute("INSERT OR IGNORE INTO Assets (name, asset_type, asset_identifier, eligible_for_bounty, instruction) VALUES (?, ?, ?, ?, ?);",(name , asset_type , asset_identifier , eligible_for_bounty , instruction))
        conn.commit()
        conn.close()



    def ProgramsTable(file , new_data):
        conn = sqlite3.connect(file) 
        query = conn.cursor()
        fetch = query.execute('SELECT * FROM Programs WHERE name = ? AND handle = ?;', (new_data['name'],new_data['handle'])).fetchone()
        if fetch : 
            column_names = [description[0] for description in query.description]
            existing_data = dict(zip(column_names, fetch))
            differences = {key: new_data[key] for key in new_data.keys() if new_data[key] != existing_data[key]}
            if differences:
                set_clause = ', '.join([f"{key} = ?" for key in differences.keys()])
                update_values = tuple(differences[key] for key in differences.keys())
                query.execute(f'''UPDATE Programs SET {set_clause} WHERE name = ?''', update_values + (new_data['name'],))
                conn.commit()
                conn.close()
                print("Program Changed :{}".format(new_data) , differences)
            else:
                pass
        else:
            query.execute(f'''INSERT INTO Programs ({', '.join(new_data.keys())}) VALUES ({', '.join(['?' for _ in new_data.keys()])})''', tuple(new_data.values()))
            conn.commit()
            conn.close()
            print("New Program Added : " , new_data)



    def ASsetsTable(file , new_data):
        conn = sqlite3.connect(file) 
        query = conn.cursor()
        fetch = query.execute('SELECT * FROM Assets WHERE name = ? AND asset_identifier = ?;', (new_data['name'], new_data['asset_identifier'] )).fetchone()
        if fetch : 
            column_names = [description[0] for description in query.description]
            existing_data = dict(zip(column_names, fetch))
            differences = {key: new_data[key] for key in new_data.keys() if key != 'asset_type' and new_data[key] != existing_data[key]}
            if differences:
                set_clause = ', '.join([f"{key} = ?" for key in differences.keys()])
                update_values = tuple(differences[key] for key in differences.keys())
                print(existing_data , update_values)
                query.execute(f'''UPDATE Assets SET {set_clause} WHERE name = ? AND asset_identifier = ?;''', update_values + (new_data['name'], new_data['asset_identifier']))
                conn.commit()
                conn.close()
                print("Asset changes : {}".format(new_data) , differences)

            else:
                pass
        else:
            try:
                query.execute(f'''INSERT INTO Assets ({', '.join(new_data.keys())}) VALUES ({', '.join(['?' for _ in new_data.keys()])})''', tuple(new_data.values()))
                conn.commit()
                conn.close()
                print("New Asset Added : " , new_data)

            except:
                pass


# Main Func
def mainFunc(url , file):
    Response = requests.get(url)
    if os.path.isfile(file):
        for program in Response.json():
            name = program['attributes']['name']
            handle = 'https://hackerone.com/'+program['attributes']['handle']
            submission_state = program['attributes']['submission_state']
            offers_bounties = program['attributes']['offers_bounties']
            if submission_state == 'pause':
                submission_state = 0
            else:
                submission_state = 1
            if offers_bounties : 
                offers_bounties = 1
            else: 
                offers_bounties = 0
            program_data = {'name': name ,'handle': handle ,'submission_state': submission_state ,'offers_bounties': offers_bounties }
            DBM.ProgramsTable(file , program_data)
            for target in program['relationships']['structured_scopes']['data']:
                asset_type = target['attributes']['asset_type']
                if asset_type == 'URL' or asset_type == 'WILDCARD':
                    asset_identifier = target['attributes']['asset_identifier']
                    eligible_for_bounty = target['attributes']['eligible_for_bounty']
                    instruction = target['attributes']['instruction']
                    if eligible_for_bounty : 
                        eligible_for_bounty = 1
                    else:
                        eligible_for_bounty = 0
                    target_data = {'name': name , 'asset_type': asset_type , 'asset_identifier': asset_identifier , 'eligible_for_bounty' : eligible_for_bounty , 'instruction': instruction}
                    DBM.ASsetsTable(file , target_data)
                else:
                    pass
    else:
        DBM.InitDB(file)
        for program in Response.json():
            name = program['attributes']['name']
            handle = 'https://hackerone.com/'+program['attributes']['handle']
            submission_state = program['attributes']['submission_state']
            offers_bounties = program['attributes']['offers_bounties']
            if submission_state == 'pause':
                submission_state = 0
            else:
                submission_state = 1
            if offers_bounties : 
                offers_bounties = 1
            else: 
                offers_bounties = 0
            for target in program['relationships']['structured_scopes']['data']:
                asset_type = target['attributes']['asset_type']
                if asset_type == 'URL' or asset_type == 'WILDCARD':
                    asset_identifier = target['attributes']['asset_identifier']
                    eligible_for_bounty = target['attributes']['eligible_for_bounty']
                    instruction = target['attributes']['instruction']
                    if eligible_for_bounty : 
                        eligible_for_bounty = 1
                    else:
                        eligible_for_bounty = 0
                    DBM.InitData(file , name , handle , submission_state , offers_bounties , asset_type , asset_identifier , eligible_for_bounty , instruction)
                else:
                    pass 



if __name__ == "__main__":
    mainFunc(Hacker01Url , 'watch.sql')
