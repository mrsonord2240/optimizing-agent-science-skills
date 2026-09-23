import subprocess,shutil,os
from pathlib import Path
root=Path(r'F:\OpenScience\audits\bio-virtual-screening\data\fresh1');root.mkdir(parents=True,exist_ok=True)
env=Path(r'F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst');smoke=env/'smoke/dock';skill=Path(r'F:\OpenScience\wt\chemoinformatics-virtual-screening\chemoinformatics\virtual-screening')
rec=root/'rec.pdb';lig=root/'lig.pdbqt';shutil.copy2(smoke/'3ptb.pdb',rec);shutil.copy2(smoke/'lig.pdbqt',lig)
child_env=os.environ.copy();child_env['PATH']=str(env/'tools/pdb2pqr-venv/Scripts')+';'+str(env/'Scripts')+';'+child_env['PATH']
subprocess.run([str(env/'Scripts/python.exe'),str(skill/'scripts/prepare_receptor.py'),str(rec),str(root/'receptor.pdbqt'),'--ph','7.4'],check=True,env=child_env)
out=root/'poses.pdbqt';run=subprocess.run([str(env/'Scripts/python.exe'),str(skill/'scripts/dock_single.py'),str(root/'receptor.pdbqt'),str(lig),'--center','-1.52','14.47','17.47','--size','20','20','20','--seed','42','--out',str(out),'--vina-exe',str(env/'tools/vina/vina.exe')],capture_output=True,text=True,check=True)
vals=[float(x) for x in run.stdout.split()];assert out.exists() and vals and all(x<0 for x in vals)
print('PREP_AND_DOCK=PASS',len(vals),min(vals))
