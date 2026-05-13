
import os
import re

def fix_views():
    path = 'blood_request/views.py'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'from django.contrib.auth.models import User' not in content:
            if 'from django.db.models import Q' in content:
                content = content.replace('from django.db.models import Q', 'from django.db.models import Q\nfrom django.contrib.auth.models import User')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {path}")
            else:
                print(f"Count not find anchor in {path}")
        else:
            print(f"{path} already fixed")
    except Exception as e:
        print(f"Error fixing {path}: {e}")

def fix_portal_layout():
    path = 'templates/portal_layout.html'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to match {{ followed by whitespace/newlines then request.user.first_name
        pattern = r'\{\{\s+request\.user\.first_name'
        replacement = '{{ request.user.first_name'
        
        new_content = re.sub(pattern, replacement, content)
        
        if content != new_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {path}")
        else:
            print(f"No changes needed for {path}")
    except Exception as e:
        print(f"Error fixing {path}: {e}")

def fix_manager_dashboard():
    path = 'templates/manager_dashboard.html'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        pattern = r'Assigned to: \{\{\s+task\.assigned_to'
        replacement = 'Assigned to: {{ task.assigned_to'
        
        new_content = re.sub(pattern, replacement, content)
        
        if content != new_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {path}")
        else:
            print(f"No changes needed for {path}")
    except Exception as e:
        print(f"Error fixing {path}: {e}")

def fix_staff_dashboard():
    path = 'templates/staff_dashboard.html'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Fix In Progress
        pattern1 = r'text-blue-800">\{\{\s+inprogress_tasks'
        replacement1 = 'text-blue-800">{{ inprogress_tasks'
        content = re.sub(pattern1, replacement1, content)
        
        # Fix Completed
        # Matches {{ done_tasks|length [newlines] }}
        pattern2 = r'\{\{\s*done_tasks\|length\s+\}\}'
        replacement2 = '{{ done_tasks|length }}'
        content = re.sub(pattern2, replacement2, content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {path}")

    except Exception as e:
        print(f"Error fixing {path}: {e}")

if __name__ == "__main__":
    fix_views()
    fix_portal_layout()
    fix_manager_dashboard()
    fix_staff_dashboard()
