import re
import evmdasm
import solcx

NORM_MAP = {
    r"PUSH\d+": "PUSH",
    r"DUP\d+":  "DUP",
    r"SWAP\d+": "SWAP",
    r"LOG\d+":  "LOG",
}

def compile_to_bytecode(sol_source: str, version: str = "0.8.0") -> str:
    solcx.set_solc_version(version)
    compiled = solcx.compile_source(
        sol_source,
        output_values=["bin-runtime"]
    )
    # grab first contract
    key = list(compiled.keys())[0]
    return compiled[key]["bin-runtime"]

def bytecode_to_opcodes(hex_bytecode: str) -> list[str]:
    if not hex_bytecode or len(hex_bytecode) < 4:
        return []
    raw = bytes.fromhex(hex_bytecode.lstrip("0x"))
    instructions = evmdasm.EvmBytecode(raw).disassemble()
    return [instr.name for instr in instructions]

def normalize_opcodes(opcodes: list[str]) -> list[str]:
    result = []
    for op in opcodes:
        matched = False
        for pattern, replacement in NORM_MAP.items():
            if re.fullmatch(pattern, op):
                result.append(replacement)
                matched = True
                break
        if not matched:
            result.append(op)
    return result

def preprocess_contract(sol_source: str, version: str = "0.8.0") -> list[str]:
    bytecode  = compile_to_bytecode(sol_source, version)
    opcodes   = bytecode_to_opcodes(bytecode)
    return normalize_opcodes(opcodes)