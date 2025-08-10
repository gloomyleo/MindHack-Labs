import importlib

def test_imports():
    modules = [
        "app",
        "dashboard_app",
        "apps.db",
        "apps.prompt_injection.service",
        "apps.deepfake_detection.service",
        "apps.ai_redteam.service",
        "apps.pqc_benchmark.service",
    ]
    for m in modules:
        importlib.import_module(m)

def test_functions_exist():
    from apps.prompt_injection.service import run_prompt_test
    from apps.deepfake_detection.service import detect_deepfake
    from apps.ai_redteam.service import plan_attack
    from apps.pqc_benchmark.service import run_benchmarks

    assert callable(run_prompt_test)
    assert callable(detect_deepfake)
    assert callable(plan_attack)
    assert callable(run_benchmarks)
