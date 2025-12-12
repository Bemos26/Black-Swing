import os

file_path = 'templates/core/index.html'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace('service-details.html', "{% url 'service_details' %}")
    new_content = new_content.replace('portfolio-details.html', "{% url 'portfolio_details' %}")
    new_content = new_content.replace('index.html', "{% url 'index' %}")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced links in index.html")
else:
    print("File not found")
