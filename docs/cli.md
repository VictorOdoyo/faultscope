# CLI

`python -m faultscope examples` lists bundled studies. `python -m faultscope study example:sequence_asymmetry` runs the default action analyze. A native JSON file or - for stdin can replace the example. --action selects a documented study; --options supplies a JSON argument object; --output saves the full result. `python -m faultscope serve --port 8768` starts the local workbench. Invalid input is JSON on stderr with exit code 2. Study records must be inspected for coordination/coverage failures; a completed calculation does not imply a protection pass.
