2. Batch processing Large Data
mandatory
Objective: Create a generator to fetch and process data in batches from the users database

Instructions:

Write a function stream_users_in_batches(batch_size) that fetches rows in batches

Write a function batch_processing() that processes each batch to filter users over the age of25`

You must use no more than 3 loops in your code. Your script must use the yield generator

Prototypes:

def stream_users_in_batches(batch_size)
def batch_processing(batch_size)
(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % cat 2-main.py                
#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % ./2-main.py | head -n 5 

{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}

{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}

{'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}

{'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102}

{'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % 

Repo:

GitHub repository: alx-backend-python
Directory: python-generators-0x00
File: 1-batch_processing.py
