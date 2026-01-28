#!/usr/bin/env python3
import subprocess
import sqlite3
import notify2
import re
import sys

def get_clipboard_text():
    """Get text from both primary selection and clipboard"""
    # Try primary selection first (highlighted text)
    try:
        result = subprocess.run(['wl-paste', '--primary', '--type', 'text/plain;charset=utf-8'],
                              capture_output=True, text=True, timeout=1)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    
    # Try clipboard (Ctrl+C)
    try:
        result = subprocess.run(['wl-paste', '--type', 'text/plain;charset=utf-8'],
                              capture_output=True, text=True, timeout=1)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    
    return ""

def lookup_notify(term):
    """Lookup term and send notification"""
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    
    c.execute('''SELECT simplified, traditional, 
                        pinyin_numbers, pinyin_marks, english 
                 FROM entries 
                 WHERE simplified=? OR traditional=?
                 LIMIT 3''', (term, term))
    
    results = c.fetchall()
    conn.close()
    
    if not results:
        notify2.init("Chinese Lookup")
        n = notify2.Notification("无结果 No match", 
                               f"'{term}' not in dictionary")
        n.show()
        return
    
    # Build notification message
    notify2.init("Chinese Lookup")
    
    lines = []
    for simp, trad, pinyin_num, pinyin_marks, eng in results[:2]:
        if simp == trad:
            lines.append(f"{simp} [{pinyin_marks}]")
        else:
            lines.append(f"{simp}/{trad} [{pinyin_marks}]")
        
        short_eng = eng[:60] + "..." if len(eng) > 60 else eng
        lines.append(f"  {short_eng}")
        lines.append("")
    
    summary = lines[0] if lines else "Lookup"
    body = "\n".join(lines[1:]) if len(lines) > 1 else "No translation"
    
    n = notify2.Notification(summary.strip(), body.strip())
    n.set_timeout(5000)
    n.show()

def main():
    text = get_clipboard_text()
    
    if not text:
        notify2.init("Chinese Lookup")
        n = notify2.Notification("No text found", 
                               "Highlight or copy Chinese text first")
        n.show()
        sys.exit(0)
    
    # Auto-copy to clipboard so it's available for pasting
    try:
        subprocess.run(['wl-copy'], input=text, text=True, timeout=1)
    except:
        pass  # Ignore if copy fails
    
    # Extract Chinese characters
    chinese_chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]{1,4}', text)
    
    if not chinese_chars:
        notify2.init("Chinese Lookup")
        n = notify2.Notification("No Chinese text", 
                               f"Found: '{text[:30]}...'")
        n.show()
        sys.exit(0)
    
    # Take first Chinese word found
    term = chinese_chars[0]
    lookup_notify(term)

if __name__ == '__main__':
    main()
