import gzip

# Open the original file in binary read mode and the output gzip file in binary write mode
with open('similarity.pkl', 'rb') as f_in:
    with gzip.open('similarity.pkl.gz', 'wb') as f_out:
        f_out.write(f_in.read())  # Read the contents of the file and write it to the compressed file
