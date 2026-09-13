#!/usr/bin/env bash
set -euo pipefail

: "${A800_SSH_ALIAS:?Set A800_SSH_ALIAS in config/local/a800.env}"
REMOTE_WORKDIR="${A800_REMOTE_WORKDIR:-~/whr}"
CONDA_ENV="${A800_CONDA_ENV:-auto_research}"

ssh "$A800_SSH_ALIAS" bash -s -- "$REMOTE_WORKDIR" "$CONDA_ENV" <<'REMOTE'
set -u
REMOTE_WORKDIR="$1"
CONDA_ENV="$2"

echo "== GPU summary =="
nvidia-smi --query-gpu=index,name,driver_version,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,pstate,compute_mode --format=csv,noheader || true

echo
echo "== GPU compute processes =="
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory --format=csv,noheader || true
nvidia-smi pmon -c 1 || true

echo
echo "== Process owners for GPU PIDs =="
PIDS="$(nvidia-smi --query-compute-apps=pid --format=csv,noheader,nounits 2>/dev/null | tr '\n' ' ')"
if [[ -n "${PIDS// /}" ]]; then
  for pid in $PIDS; do
    ps -o user=,pid=,etime=,cmd= -p "$pid" || true
  done
else
  echo "No compute PIDs reported."
fi

echo
echo "== CPU / memory / load =="
uptime || true
nproc || true
free -h || true

echo
echo "== Disk =="
df -h / "$HOME" "$REMOTE_WORKDIR" 2>/dev/null || true

echo
echo "== Scheduler =="
if command -v squeue >/dev/null 2>&1; then
  squeue -a
else
  echo "Slurm not found."
fi

echo
echo "== Python / Conda =="
python3 --version || true
conda --version || true
conda env list || true
if conda env list 2>/dev/null | awk '{print $1}' | grep -qx "$CONDA_ENV"; then
  conda run -n "$CONDA_ENV" python --version || true
else
  echo "Conda env '$CONDA_ENV' not found."
fi
REMOTE
