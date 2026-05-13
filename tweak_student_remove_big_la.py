from pathlib import Path
p=Path('/root/.openclaw/workspace/render_student_photo_school_post_v2.py')
s=p.read_text()
# Remove big solo LA stamp/composition from the student photo post, keeping only official top logo.
s=s.replace("<div class=\"laSolo\"><img src=\"assets/la-solo.svg\"></div>", "")
p.write_text(s)
