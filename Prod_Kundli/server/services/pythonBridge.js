const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * Resolves the appropriate Python executable path.
 */
function getPythonExecutable() {
  if (process.env.PYTHON_BIN && fs.existsSync(process.env.PYTHON_BIN)) {
    return process.env.PYTHON_BIN;
  }

  const candidatePaths = [
    path.resolve(__dirname, '../../.venv/bin/python'), // Prod_Kundli/.venv
    path.resolve(__dirname, '../../../.venv/bin/python'), // Root .venv (Linux)
    path.resolve(__dirname, '../../.venv/Scripts/python.exe'), // Windows local
    path.resolve(__dirname, '../../../.venv/Scripts/python.exe'), // Root Windows local
    '/usr/bin/python3',
    'python3',
    'python'
  ];

  for (const p of candidatePaths) {
    if (p.includes('/') || p.includes('\\')) {
      if (fs.existsSync(p)) {
        return p;
      }
    } else {
      return p; // Command in PATH
    }
  }
  return 'python3';
}

/**
 * Executes python_bridge.py with a JSON payload and returns the parsed result.
 */
function executePythonBridge(payload) {
  return new Promise((resolve, reject) => {
    const pythonBin = getPythonExecutable();
    const bridgeScript = path.resolve(__dirname, '../../python_engine/python_bridge.py');

    const pyProcess = spawn(pythonBin, [bridgeScript], {
      env: {
        ...process.env,
        PYTHONUNBUFFERED: '1'
      }
    });

    let stdoutData = '';
    let stderrData = '';

    pyProcess.stdout.on('data', (chunk) => {
      stdoutData += chunk.toString();
    });

    pyProcess.stderr.on('data', (chunk) => {
      stderrData += chunk.toString();
    });

    pyProcess.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`Python Engine Error (Code ${code}): ${stderrData || 'Unknown error'}`));
      }

      try {
        const parsed = JSON.parse(stdoutData);
        resolve(parsed);
      } catch (err) {
        reject(new Error(`Failed to parse calculation output: ${err.message}. Raw: ${stdoutData.substring(0, 300)}`));
      }
    });

    pyProcess.on('error', (err) => {
      reject(new Error(`Failed to spawn Python process [${pythonBin}]: ${err.message}`));
    });

    // Write input payload to stdin and close
    pyProcess.stdin.write(JSON.stringify(payload));
    pyProcess.stdin.end();
  });
}

/**
 * Calculates complete Vedic & KP Kundli report.
 */
async function calculateKundli(birthData) {
  return executePythonBridge({
    action: 'generate',
    birth: birthData
  });
}

/**
 * Calculates 36-Gun Ashtakoota Marriage Matching.
 */
async function calculateMatching(groomData, brideData) {
  return executePythonBridge({
    action: 'matching',
    groom: groomData,
    bride: brideData
  });
}

module.exports = {
  calculateKundli,
  calculateMatching,
  getPythonExecutable
};
