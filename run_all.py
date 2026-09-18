"""Everything this companion claims, in one command: the three exams, then every
figure and both animations, regenerated into assets/.

    python run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIGURES = ["article_worked.py", "article_tables.py", "article_signing.py",
           "article_who_signs.py", "article_gifs.py"]


def main() -> None:
    print("=" * 72)
    print("THE EXAMS (table_logic.py)")
    print("=" * 72)
    subprocess.run([sys.executable, str(HERE / "table_logic.py")], check=True, cwd=HERE)
    print()
    print("=" * 72)
    print("THE FIGURES (written into assets/)")
    print("=" * 72)
    for script in FIGURES:
        print("--", script)
        subprocess.run([sys.executable, str(HERE / script)], check=True, cwd=HERE)


if __name__ == "__main__":
    main()
