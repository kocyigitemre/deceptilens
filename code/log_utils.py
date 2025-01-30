def write_log(log_path, log_data):
    """Writes log data to a file."""
    with open(log_path, 'a') as log_file:
        log_file.write(log_data + '\n')
