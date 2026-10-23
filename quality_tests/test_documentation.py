"""
Quality Test: Documentation
Documentation generation system testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.documentation import (
    DocumentationGenerator,
    DocumentationType,
    DocStyle,
    DocTemplate,
    DocumentationResult
)


def test_generate_docstring():
    """
    Test: Generate docstring.
    """
    print("=" * 70)
    print("TEST: Generate Docstring")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function(x, y):
    return x + y
""", encoding='utf-8')
        
        generator = DocumentationGenerator()
        
        # Generate docstring
        result = generator.generate_docstring(str(test_file), line=2, column=0)
        
        assert result.success, "Generation başarılı olmalı"
        assert result.documentation is not None, "Documentation olmalı"
        assert "Args:" in result.documentation or "Parameters:" in result.documentation, "Args içermeli"
        
        print(f"  Success: {result.success}")
        print(f"  Documentation length: {len(result.documentation)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Generate docstring")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_generate_function_docs():
    """
    Test: Generate function documentation.
    """
    print("=" * 70)
    print("TEST: Generate Function Documentation")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function(x, y):
    return x + y
""", encoding='utf-8')
        
        generator = DocumentationGenerator()
        
        # Generate function docs
        result = generator.generate_function_docs("my_function", str(test_file))
        
        assert result.success, "Generation başarılı olmalı"
        assert result.documentation is not None, "Documentation olmalı"
        assert "my_function" in result.documentation, "Function name içermeli"
        
        print(f"  Success: {result.success}")
        print(f"  Documentation length: {len(result.documentation)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Generate function documentation")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_generate_class_docs():
    """
    Test: Generate class documentation.
    """
    print("=" * 70)
    print("TEST: Generate Class Documentation")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
class MyClass:
    def method(self):
        pass
""", encoding='utf-8')
        
        generator = DocumentationGenerator()
        
        # Generate class docs
        result = generator.generate_class_docs("MyClass", str(test_file))
        
        assert result.success, "Generation başarılı olmalı"
        assert result.documentation is not None, "Documentation olmalı"
        assert "Attributes:" in result.documentation or "Methods:" in result.documentation, "Attributes/Methods içermeli"
        
        print(f"  Success: {result.success}")
        print(f"  Documentation length: {len(result.documentation)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Generate class documentation")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_generate_module_docs():
    """
    Test: Generate module documentation.
    """
    print("=" * 70)
    print("TEST: Generate Module Documentation")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    pass

class MyClass:
    pass
""", encoding='utf-8')
        
        generator = DocumentationGenerator()
        
        # Generate module docs
        result = generator.generate_module_docs(str(test_file))
        
        assert result.success, "Generation başarılı olmalı"
        assert result.documentation is not None, "Documentation olmalı"
        assert "test_module" in result.documentation, "Module name içermeli"
        
        print(f"  Success: {result.success}")
        print(f"  Documentation length: {len(result.documentation)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Generate module documentation")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_generate_markdown_docs():
    """
    Test: Generate markdown documentation.
    """
    print("=" * 70)
    print("TEST: Generate Markdown Documentation")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    pass
""", encoding='utf-8')
        
        generator = DocumentationGenerator()
        
        # Generate markdown docs
        result = generator.generate_markdown_docs(str(test_file))
        
        assert result.success, "Generation başarılı olmalı"
        assert result.documentation is not None, "Documentation olmalı"
        assert "#" in result.documentation, "Markdown header içermeli"
        
        print(f"  Success: {result.success}")
        print(f"  Documentation length: {len(result.documentation)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Generate markdown documentation")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_documentation_type_enum():
    """
    Test: DocumentationType enum.
    """
    print("=" * 70)
    print("TEST: DocumentationType Enum")
    print("=" * 70)
    
    assert DocumentationType.DOCSTRING.value == "docstring"
    assert DocumentationType.MARKDOWN.value == "markdown"
    assert DocumentationType.API.value == "api"
    assert DocumentationType.README.value == "readme"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(DocumentationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentationType enum")
    print("=" * 70)


def test_doc_style_enum():
    """
    Test: DocStyle enum.
    """
    print("=" * 70)
    print("TEST: DocStyle Enum")
    print("=" * 70)
    
    assert DocStyle.GOOGLE.value == "google"
    assert DocStyle.NUMPY.value == "numpy"
    assert DocStyle.SPHINX.value == "sphinx"
    assert DocStyle.PEP257.value == "pep257"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(DocStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: DocStyle enum")
    print("=" * 70)


def test_doc_template_dataclass():
    """
    Test: DocTemplate dataclass.
    """
    print("=" * 70)
    print("TEST: DocTemplate Dataclass")
    print("=" * 70)
    
    template = DocTemplate(
        name="test_template",
        description="Test template",
        template="Template content",
        style=DocStyle.GOOGLE
    )
    
    assert template.name == "test_template", "Name eşleşmeli"
    assert template.style == DocStyle.GOOGLE, "Style eşleşmeli"
    
    print(f"  Name: {template.name}")
    print(f"  Style: {template.style.value}")
    
    print("\n" + "=" * 70)
    print("PASS: DocTemplate dataclass")
    print("=" * 70)


def test_documentation_result_dataclass():
    """
    Test: DocumentationResult dataclass.
    """
    print("=" * 70)
    print("TEST: DocumentationResult Dataclass")
    print("=" * 70)
    
    result = DocumentationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentationResult dataclass")
    print("=" * 70)


def test_google_style():
    """
    Test: Google doc style.
    """
    print("=" * 70)
    print("TEST: Google Doc Style")
    print("=" * 70)
    
    generator = DocumentationGenerator(style=DocStyle.GOOGLE)
    
    assert generator.style == DocStyle.GOOGLE, "Google style olmalı"
    
    print(f"  Style: {generator.style.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Google doc style")
    print("=" * 70)


def test_numpy_style():
    """
    Test: Numpy doc style.
    """
    print("=" * 70)
    print("TEST: Numpy Doc Style")
    print("=" * 70)
    
    generator = DocumentationGenerator(style=DocStyle.NUMPY)
    
    assert generator.style == DocStyle.NUMPY, "Numpy style olmalı"
    
    print(f"  Style: {generator.style.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Numpy doc style")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_generate_docstring()
        test2 = test_generate_function_docs()
        test3 = test_generate_class_docs()
        test4 = test_generate_module_docs()
        test5 = test_generate_markdown_docs()
        test6 = test_documentation_type_enum()
        test7 = test_doc_style_enum()
        test8 = test_doc_template_dataclass()
        test9 = test_documentation_result_dataclass()
        test10 = test_google_style()
        test11 = test_numpy_style()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Generate Docstring: {'PASS' if test1 else 'FAIL'}")
        print(f"Generate Function Docs: {'PASS' if test2 else 'FAIL'}")
        print(f"Generate Class Docs: {'PASS' if test3 else 'FAIL'}")
        print(f"Generate Module Docs: {'PASS' if test4 else 'FAIL'}")
        print(f"Generate Markdown Docs: {'PASS' if test5 else 'FAIL'}")
        print(f"DocumentationType Enum: {'PASS' if test6 else 'FAIL'}")
        print(f"DocStyle Enum: {'PASS' if test7 else 'FAIL'}")
        print(f"DocTemplate Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"DocumentationResult Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"Google Style: {'PASS' if test10 else 'FAIL'}")
        print(f"Numpy Style: {'PASS' if test11 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11])
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
