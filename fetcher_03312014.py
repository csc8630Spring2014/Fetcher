# Fetcher for fasta sequences of the rcsb pdb bank
#
# Explanation of cath id tag:
#	<CATH_ID>[('00', '1.10.490.10')]</CATH_ID>
#	'00' is domain id
#	'1.10.490.10' is cath id for the domain.
#	It is possible to have several domains within a chain
# Example entries
#
# Chain of amino acid with only one domain.
#	<PROTEIN>
#	<PDBID_WITH_CHAIN_ID>101m_A</PDBID_WITH_CHAIN_ID>
#	<NAME>MYOGLOBIN</NAME>
#	<CATH_ID>[('00', '1.10.490.10')]</CATH_ID>
#	<SEQUENCE>MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG</SEQUENCE>
#	</PROTEIN>
#
# Chain of amino acid with two domains
#	<PROTEIN>
#	<PDBID_WITH_CHAIN_ID>10gs_B</PDBID_WITH_CHAIN_ID>
#	<NAME>GLUTATHIONE S-TRANSFERASE P1-1</NAME>
#	<CATH_ID>[('02', '1.20.1050.10'), ('01', '3.40.30.10')]</CATH_ID>
#	<SEQUENCE>PPYTVVYFPVRGRCAALRMLLADQGQSWKEEVVTVETWQEGSLKASCLYGQLPKFQDGDLTLYQSNTILRHLGRTLGLYGKDQQEAALVDMVNDGVEDLRCKYISLIYTNYEAGKDDYVKALPGQLKPFETLLSQNQGGKTFIVGDQISFADYNLLDLLLIHEVLAPGCLDAFPLLSAYVGRLSARPKLKAFLASPEYVNLPINGNGKQ</SEQUENCE>
#	</PROTEIN>

import urllib
import string
import re

#pdb_sequence_url = 'ftp://ftp.rcsb.org/pub/pdb/derived_data/pdb_seqres.txt'
#pdb_sequence_url_handle = urllib.urlopen(pdb_sequence_url)
pdb_sequence_url_handle = open('pdb_seqres.txt')
# read line by line

name_exist = False

output_xml_name = 'pdb_sequences_xml.xml'
output_xml_handle = open(output_xml_name, 'w+')

sequence_now = ''

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
            tokens = line.split()
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

writing_buffer = ''
old_writing_buffer = ''

for line in pdb_sequence_url_handle:
    if '>' in line:
        if name_exist == False:
            line_split = line.split()
            pdb_id_with_chain_id_now = line_split[0][1:7]
            mol_type = line_split[1][4:]
            print "mol_type", mol_type
            #print "#split line: ", line_split

            if len(line_split) > 3:
                name_first_word = line_split[3] # that is the first word in the name, as seperated by space.
                name_now = line[line.find(name_first_word):-1] # the -1 removes the \n at the end.
            else:
                name_now = ''

            if sequence_now != '':
                # This writes the sequence of the pdbid of **previous** iteration
                writing_buffer += '<SEQUENCE>%s</SEQUENCE>\n' % sequence_now
                writing_buffer += '</PROTEIN>\n'
                if mol_type == 'protein':
                    output_xml_handle.write( writing_buffer )
                    print "written: "
                    print writing_buffer
            writing_buffer = '<PROTEIN>\n'

            writing_buffer += '<PDBID_WITH_CHAIN_ID>%s</PDBID_WITH_CHAIN_ID>\n' % pdb_id_with_chain_id_now
            writing_buffer += '<NAME>%s</NAME>\n' % name_now
            #print "#line: ", line
            #if __name__ == '__main__':
    	    p = get_pdb_dict()
            s = pdb_id_with_chain_id_now
            x = s = s.replace('_', '')
            #chains to iterate through pdb sequence file
    	    try:
                chains = p[x]
                writing_buffer += '<CATH_ID>%s</CATH_ID>\n' % chains
            #if chains != KeyError:
            except KeyError:
                pass
    	    #following to output the CATH id into xml format
    	        
            #print "#result: ", pdb_id_with_chain_id_now, name_now, sequence_now
            sequence_now = ''
            name_exist = True
    else:
        sequence_now += line[:-1] # removes \n at the end
        name_exist = False

if sequence_now != '':
    # Since 'writes the sequence of the pdbid of **previous** iteration', need to write the last sequence.
    output_xml_handle.write('<SEQUENCE>%s</SEQUENCE>\n</PROTEIN>\n' % sequence_now)

output_xml_handle.close()
