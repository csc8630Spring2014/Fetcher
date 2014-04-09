import re


def get_pdb_dict():
    """Takes CATH domain list and returns dictionary of PDB codes
    & their CATH families"""
    pdbs = {}
    fh = open('CathDomainList', 'r')
    lines = fh.read().split('\n')
    fh.close()
    for line in lines:
        #ignore comments
        if not line.startswith('#'):
            #tokens = line.split()
            #lines are space-delimited, so need re.split() here
            tokens = re.split('\s+', line)
            pdb = tokens[0]
            #split the PDB into root identifier and chain id
            pdb_root = pdb[0:5]
            pdb_chain = pdb[5:]
            #could be more/less precise by using more/fewer columns
            cath = '.'.join(tokens[1:5])
            try:
                pdbs[pdb_root].append((pdb_chain,cath))
            except KeyError:
                pdbs[pdb_root] = [(pdb_chain,cath)]
    return pdbs

def getAllProtiens(filename, pdbs):
    with open(filename,"r") as fp:
        while True:
            title = fp.readline()
            pdb_id = title[1:5]+title[6:5]
            print title
            seq = fp.readline()
            if len(seq) < 50 or len(seq) > 500:
                continue
            if(title[13]!='p'):
                continue
            cathid = ''
            if pdbid in pdb_dict:
                cathid = pdbs[pdb_id]
            if pdb_id.trim() == "":
                break
            yield pdb_id, cathid, seq


def writeXML(filename,stream):
    with open(filename,"w") as fp:
        for pid, cid, seq in stream:
            output = "<PROTEIN>\n"
            output += "<PDBID>"+str(pid)+"</PDBID>\n"
            output += "<CATHID>"+str(cid)+"</CATHID>\n"
            output += "<SEQUENCE>\n"+str(seq)+"\n</SEQUENCE>\n"
            output ++ "</PROTEIN>\n"
            fp.write(output)

pdb_dict = get_pdb_dict()
writeXML("test_output.xml",getAllProtiens("pdb_seqres.txt",pdb_dict))


