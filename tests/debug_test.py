import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("1. Starting script...")

try:
    print("2. Importing modules...")
    from core import pdeco
    from database import cast_db_manager
    print("3. Imports successful")
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("4. Getting cast info...")
    cast_info = cast_db_manager.get_cast_info('きら')
    print(f"5. Cast info: {cast_info}")
    if cast_info:
        print(f"6. Cast info length: {len(cast_info)}")
        if len(cast_info) > 5:
            print(f"7. pdeco_url: {cast_info[5]}")
        else:
            print(f"7. Cast info doesn't have index 5")
    else:
        print("7. Cast info is None or empty")
    
    print("8. Calling pdeco_easy_login...")
    result = pdeco.pdeco_easy_login('きら', False)
    print(f"9. Result: {result}")
    print(f"10. Result type: {type(result)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("11. Script completed successfully")

