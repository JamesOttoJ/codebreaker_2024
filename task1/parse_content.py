#!/usr/bin/python3

with open("content.txt") as content_file:
    with open("out.csv", "w") as out_file:
        out_file.write("company,address,person 1 name,person 1 number,person 1 email,person 2 name,person 2 number,person 2 email,id,date\n")
        while True:
            company = content_file.readline()
            if not company:
                break
            company = company.rstrip()
            address = content_file.readline()
            if not address:
                break
            address = address.rstrip()
            person_1_name = content_file.readline()
            if not person_1_name:
                break
            person_1_name = person_1_name.rstrip()
            person_1_number = content_file.readline()
            if not person_1_number:
                break
            person_1_number = person_1_number.rstrip()
            person_1_email = content_file.readline()
            if not person_1_email:
                break
            person_1_email = person_1_email.rstrip()
            person_2_name = content_file.readline()
            if not person_2_name:
                break
            person_2_name = person_2_name.rstrip()
            person_2_number = content_file.readline()
            if not person_2_number:
                break
            person_2_number = person_2_number.rstrip()
            person_2_email = content_file.readline()
            if not person_2_email:
                break
            person_2_email = person_2_email.rstrip()
            trans_id = content_file.readline()
            if not trans_id:
                break
            trans_id = trans_id.rstrip()
            date = content_file.readline()
            if not date:
                break
            date = date.rstrip()
            out_file.write("\"" + company + "\",\"" + address + "\",\"" + person_1_name + "\",\"" + person_1_number + "\",\"" + person_1_email + "\",\"" + person_2_name + "\",\"" + person_2_number + "\",\"" + person_2_email + "\",\"" + trans_id + "\",\"" + date + "\"\n")
