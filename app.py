from flask import Flask, render_template, request

app = Flask(__name__)

def audit_plsql_code(code: str):
    import re
    results = []
    score = 100

    # Rule 1: Comments check
    if re.search(r'--|/\*.*?\*/', code, re.DOTALL):
        results.append("✅ Good: Comments are present.")
    else:
        results.append("⚠️ Warning: No comments found. Code should be properly documented.")
        score -= 10

    # Rule 2: Hard-coded strings
    if re.search(r"'.+?'", code):
        results.append("⚠️ Warning: Hard-coded string literals detected.")
        score -= 10
    else:
        results.append("✅ Good: No hard-coded string literals found.")

    # Rule 3: Hard-coded numbers
    if re.search(r':=\s*[2-9]\d*', code):
        results.append("⚠️ Warning: Hard-coded numbers detected.")
        score -= 5
    else:
        results.append("✅ Good: No suspicious hard-coded numbers found.")

    # Rule 4: Exception handling
    if "EXCEPTION" in code.upper():
        results.append("✅ Good: Exception block is present.")
    else:
        results.append("⚠️ Warning: No EXCEPTION block found.")
        score -= 10

    # Rule 5: SELECT INTO check
    if re.search(r'\bSELECT\b.+\bINTO\b', code, re.IGNORECASE | re.DOTALL):
        results.append("✅ Good: SELECT INTO statement used correctly.")
    else:
        results.append("⚠️ Warning: SELECT INTO statement not used.")
        score -= 5

    # Rule 6: Variable declarations
    if re.search(r'\bDECLARE\b.*\b[A-Za-z_]+\s+(NUMBER|VARCHAR2|DATE)', code, re.IGNORECASE | re.DOTALL):
        results.append("✅ Good: Variables are properly declared.")
    else:
        results.append("⚠️ Warning: Variable declarations missing or incomplete.")
        score -= 5

    # Rule 7: Output to DBMS
    if re.search(r'DBMS_OUTPUT\.PUT_LINE', code, re.IGNORECASE):
        results.append("✅ Good: Output is displayed using DBMS_OUTPUT.")
    else:
        results.append("⚠️ Warning: No DBMS_OUTPUT.PUT_LINE used for output display.")
        score -= 5

    # Rule 8: Indentation
    if re.search(r'\n\s{2,}', code):
        results.append("✅ Good: Code uses proper indentation.")
    else:
        results.append("⚠️ Warning: Code formatting could be improved (no indentation).")
        score -= 5

    # Rule 9: BEGIN ... END block
    if re.search(r'\bBEGIN\b.*\bEND\b;', code, re.IGNORECASE | re.DOTALL):
        results.append("✅ Good: BEGIN ... END block is correctly used.")
    else:
        results.append("❌ Error: BEGIN ... END block missing or malformed.")
        score -= 15

    # Rule 10: RAISE_APPLICATION_ERROR suggestion
    if "RAISE_APPLICATION_ERROR" in code.upper():
        results.append("✅ Good: Custom error handling used via RAISE_APPLICATION_ERROR.")
    else:
        results.append("ℹ️ Info: You may consider using RAISE_APPLICATION_ERROR for better error reporting.")

    score = max(0, min(score, 100))
    return results, score


@app.route('/', methods=['GET', 'POST'])
def index():
    audit_results = []
    score = None
    code = ""

    if request.method == 'POST':
        code = request.form['plsql_code']
        audit_results, score = audit_plsql_code(code)

    return render_template('index.html', audit_results=audit_results, score=score, code=code)


if __name__ == '__main__':
    app.run(debug=True)
