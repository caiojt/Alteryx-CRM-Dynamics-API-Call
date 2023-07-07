import os
import zipfile
import paramiko
import pandas as pd
import datetime as dt
import shutil

# Provide the path and filename for the ZIP file
zip_path = 'YOUR_PATH'
directory_path = 'YOUR_PATH'
date_today = dt.datetime.now()
directory_path_file = f'YOUR_PATH_{date_today.date()}.csv'

#SFTP details
remote_path = f'YOUR_PATH{date_today.date()}.zip'
hostname = 'FTP_HOST'
port = 22  # Default SFTP port is 22
username = 'USER_NAME'
password = 'PASSWORD'

data = ['new output']


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting file '{file_path}': {e}")

def delete_staging_folders(path):
    try:
        shutil.rmtree(path)
        print(f"Folder '{path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting folder '{path}': {e}")

def converts_df_zip_file(df):
    # Convert DataFrame to CSV format
    csv_data = df.to_csv(index=False)
    print('Data converted')

    permissions = 0o777
    os.makedirs(directory_path, exist_ok=True)
    os.chmod(directory_path, permissions)

    # Write the CSV data to the file
    csv_file = os.path.join(directory_path, f'plane_cp_data_{date_today.date()}.csv')

    with open(csv_file, 'w') as f:
        f.write(csv_data)
    print('CSV file written')

def zip_directory(directory_path_file, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path_file):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_path_file))
    print('Directory zipped')


def send_via_sftp(zip_path, remote_path, hostname, port, username, password):
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(zip_path, remote_path)
    sftp.close()
    transport.close()
    print('File sent via SFTP!')


# main code
df = pd.DataFrame(data)
converts_df_zip_file(df)
zip_directory(directory_path, zip_path)
send_via_sftp(zip_path, remote_path, hostname, port, username, password)
delete_staging_folders(directory_path)
delete_file(zip_path)
