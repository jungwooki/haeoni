"""Public filenames shared by page builders and navigation."""
DEPARTMENT_FILES = {'child': 'kids10.html', 'women': 'woman1.html', 'pain': 'pain1.html'}
RENAMED_PAGES = {'kids10.html', 'rhini1.html', 'woman1.html', 'pain1.html'}
def department_file(dept):
 return DEPARTMENT_FILES.get(dept, 'clinic-' + dept + '.html')
def is_clinic_page(name):
 return name in RENAMED_PAGES or name.startswith(('clinic-', 'internal-', 'child-', 'women-'))
def is_hub(name):
 return name.startswith('clinic-') or name in {'kids10.html', 'woman1.html', 'pain1.html'}
