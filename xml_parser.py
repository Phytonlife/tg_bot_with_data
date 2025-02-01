import xmltodict

def parse_xml_jobs(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        data = xmltodict.parse(file.read())
        jobs = []
        for job in data['jobs']['job']:
            jobs.append({
                'title': job['title'],
                'description': job['description'],
                'company': job['company'],
                'location': job.get('location', ''),
                'end_date': job['end_date']
            })
        return jobs