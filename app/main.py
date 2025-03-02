import sys
import os
import zlib
import hashlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif (command == "cat-file") and (sys.argv[2] == "-p"): 
        # git's internal command `git cat-file` for viewing  content of an objects
        blob_sha = sys.argv[3] # The compressed SHA1 file added on git
        with open(f".git/objects/{blob_sha[:2]}/{blob_sha[2:]}", "rb") as outfile:
            # git takes the sha1 of the content to be written, takes the first two characters, 
            # in this case 4c, creates a folder and then uses the rest of it as the filename
            # read more here: https://blog.meain.io/2023/what-is-in-dot-git/
            compressed_blob = outfile.read()
            decompressed_blob = zlib.decompress(compressed_blob)
            blob_content = decompressed_blob.split(b"\0")[1]
            decoded_blob = blob_content.decode()
            # print(f"Reading from: {compressed_blob}")
            # print(f"=============================================================")
            print(decoded_blob, end="")  
    elif (command == "hash-object") and (sys.argv[2] == "-w"):
        # git hash-object is used to compute the SHA hash of a Git object
        try:
            # Check if you are in the git worktree 
            if not os.path.isdir(".git"):
                print("fatal: not a git repository (or any of the parent directories): \
                      .git", file=sys.stderr)
                sys.exit(1)
                
            # If we get here, we're in a git worktree 
            file_path sys.argv[3]
            with open(file_path, "rb") as infile:
                file_content = infile.read()
                
                
            # prepare a blob content 
            header = b"blob {len(file_content)}\0".encode()
            store = header + file_content
            
            # Calculate SHA1 hash 
            sha = hashlib.sha1(store).hexdigest()
            
            # Compress the content
            compressed = zib.compress(store)
            
            # Create and save the sha1 object directory 
            directory = f".git/objects/{sha[:2]}"
            if not os.path.exists(directory):
                os.mkdir(directory)
                
            with open(f"{directory}/{sha[2:]}", "wb") as f:
                f.write(compressed)
                
                # Ensure that the file has been written in the directory
                # assert(os.path.exists(compressed))
                
            print(sha, end="")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
