from app.tools.code_patch_applier import CodePatchApplier


applier = CodePatchApplier()


old_code = '''def hello():
    print("ESKI")'''


new_code = '''def hello():
    print("YENI")'''


result = applier.apply_patch(
    "patch_test.py",
    old_code,
    new_code,
)


print(result)
