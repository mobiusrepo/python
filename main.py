from fastapi import FastAPI, UploadFile, File
from fastapi.responses import PlainTextResponse
import json, os, subprocess
from pi_model import load_json, json_to_pi_per_function, system_to_pi
from conversion_to_promela import convert_pi_to_promela

# --- Import your modules ---

# app = FastAPI()
app = FastAPI(title="Mobius PI-CALCULUS-API", root_path="/mobius-pi-calculus")
# app = FastAPI(title="Mobius PI-CALCULUS-API", root_path="/mobius-pi-caluculas")



# Use current working directory for all file operations
BASE_DIR = os.getcwd()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Pi Calculus API's!"}

# ------------------------------------------------------------
# 1. Convert high-level agent JSON to π-calculus JSON
# ------------------------------------------------------------
@app.post("/pi_model/")
async def convert_json(file: UploadFile = File(...)):
    file_path = os.path.join(BASE_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    # Add the missing logic:
    try:
        agents = load_json(file_path)  # from pi_model.py
        pi_output = json_to_pi_per_function(agents)  # from pi_model.py
        system_pi = system_to_pi(agents)  # from pi_model.py
        
        return {
            "agents": pi_output,
            "system": system_pi,
            "message": "JSON successfully converted to pi-calculus"
        }
    except Exception as e:
        return {"error": f"Failed to process JSON: {str(e)}"}

@app.post("/conversion_to_promela/")
async def json_to_promela(file: UploadFile = File(...)):
    """Converts π-calculus JSON into a Promela model (.pml)"""
    file_path = os.path.join(BASE_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())


    base_name = os.path.splitext(file.filename)[0]
    output_filename = f"{base_name}_promela_code.pml"
    output_path = os.path.join(BASE_DIR, output_filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            input_json = json.load(f)
        promela_text = convert_pi_to_promela(input_json)
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(promela_text)
    return {
        "filename": output_filename,
        "output_directory": BASE_DIR,
        "promela_content": promela_text
    }








# ------------------------------------------------------------
# 3. Deadlock Checking
# ------------------------------------------------------------
@app.post("/check_deadlock/", response_class=PlainTextResponse)
async def check_deadlock(file: UploadFile = File(...)):
    """Run SPIN to check for deadlocks"""
    file_path = os.path.join(BASE_DIR, file.filename)








    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step 1: spin -a file.pml
    try:
        subprocess.run(["spin", "-a", file_path],
                       cwd=BASE_DIR, check=True,
                       capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        return f"Spin generation failed:\n{e.stderr or e.stdout}"

    # Step 2: gcc -o pan pan.c

    try:
        subprocess.run(["gcc", "-o", "pan", "pan.c"],
                       cwd=BASE_DIR, check=True,
                       capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        return f"Compilation failed:\n{e.stderr or e.stdout}"

    # Step 3: ./pan

    try:
        result = subprocess.run(["./pan"],
                                cwd=BASE_DIR, capture_output=True, text=True)
        output_text = result.stdout or result.stderr
    except FileNotFoundError:
        return "Error: pan not found."
    except subprocess.CalledProcessError as e:
        output_text = e.stdout + "\n" + e.stderr


    summary = "✅ No deadlocks detected." if "errors: 0" in output_text else "⚠️ Deadlock or errors detected!"
    return f"{summary}\n\nFiles saved in: {BASE_DIR}\n\n--- SPIN Output ---\n{output_text}"


# ------------------------------------------------------------
# 4. Liveness Checking
# ------------------------------------------------------------
@app.post("/check_liveness/", response_class=PlainTextResponse)
async def check_liveness(file: UploadFile = File(...)):
    """Run SPIN to check for liveness"""
    file_path = os.path.join(BASE_DIR, file.filename)







    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step 1: spin -a file.pml
    try:
        subprocess.run(["spin", "-a", file_path],
                       cwd=BASE_DIR, check=True,
                       capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        return f"Spin generation failed:\n{e.stderr or e.stdout}"

    # Step 2: gcc -o pan pan.c

    try:
        subprocess.run(["gcc", "-o", "pan", "pan.c"],
                       cwd=BASE_DIR, check=True,
                       capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        return f"Compilation failed:\n{e.stderr or e.stdout}"

    # Step 3: ./pan -a

    try:
        result = subprocess.run(["./pan", "-a"],
                                cwd=BASE_DIR, capture_output=True, text=True)
        output_text = result.stdout or result.stderr
    except FileNotFoundError:
        return "Error: pan not found."
    except subprocess.CalledProcessError as e:
        output_text = e.stdout + "\n" + e.stderr


    if "acceptance cycle" in output_text or "errors: 1" in output_text:
        summary = "⚠️ Liveness violation detected (acceptance cycle found)."
    elif "errors: 0" in output_text:
        summary = "✅ No liveness violations detected."
    else:
        summary = "ℹ️ Could not determine liveness result."

    return f"{summary}\n\nFiles saved in: {BASE_DIR}\n\n--- SPIN Output ---\n{output_text}"




