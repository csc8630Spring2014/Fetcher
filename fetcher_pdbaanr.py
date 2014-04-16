import re

def get_cath():
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


def writeXML(filename,stream):
    with open(filename,"w") as fp:
        for pid, cid, seq in stream:
            #print pid
            output = "<PROTEIN>\n"
            output += "<PDBID>"+str(pid)+"</PDBID>\n"
            output += "<CATHID>"+str(cid)+"</CATHID>\n"
            output += "<SEQUENCE>\n"+str(seq)+"</SEQUENCE>\n"
            output += "</PROTEIN>\n"
            fp.write(output)



def readPdbaanrFastaHeader( pdbaanr_fasta_header ):
    # Example of pdbaanr fasta header:
    #     >1JU8A 37 NMR NA NA NA no Leginsulin <UNP ALB1_SOYBN> [NA]
    # ** Assumes the header is single line **

    pdb_id_with_chain_id = pdbaanr_fasta_header[1:5].lower() + pdbaanr_fasta_header[5].upper()
    split_list = pdbaanr_fasta_header.split()
    sequence_length = int( split_list[1] )
    return pdb_id_with_chain_id, sequence_length

def readPdbaanr(filename, cath_id_dict):
    # Structure of pdbaanr
    #   1. header (which has '>')
    #   2. Several lines (we don't know how many lines) of sequences
    #   3. back to step 1.

    # Note that everything in pdbaanr are proteins:
    # "every protein chain in every PDB file has a unique entry in pdbaa.gz."

    # So, this function would read data of the last entry and parse them.
    # Then, when it encounters the header of this entry, it would write the parsed data of last entry.
    # Before parsing this entry.
    # and then repeats.

    reading_first_entry = True
    sequence_now = ''
    for line_now in open(filename,"r"):
        # assumes that the header only has a single line
        #line_now  = fp.readline()
        # Check if the line is a FASTA header (that is, if it has '>')
        if '>' in line_now:
            ## Write data for the last entry.
            if reading_first_entry == True:
                reading_first_entry = False # if we are reading first entry, then there is no last entry to parse.
            else:

                ####################
                # write last entry #
                ####################
                #pdb_id_with_chain_id_now, cathid_now

                if sequence_length_now > 50 and sequence_length_now < 500:
                    print pdb_id_with_chain_id_now
                    try:
                        cathid_now = cath_id_dict[pdb_id_with_chain_id_now]
                    except KeyError:
                        cathid_now = ''
                        print "no cath id"

                    if len( sequence_now ) != sequence_length_now:
                        print "sequence length check failed"

                    print sequence_now

                    yield pdb_id_with_chain_id_now, cathid_now, sequence_now

                #yield pdb_id_with_chain_id_now, cathid_now, sequence_now

                ####################
                # parse this entry #
                ####################

               ## Parse current entry.
            sequence_now = ''     # reinitialize sequence buffer.
                ## we are reading a header
            pdb_id_with_chain_id_now, sequence_length_now = readPdbaanrFastaHeader( line_now )
        else:
            sequence_now += line_now[:-1]    # the [:-1] is to get rid of the '\n' (newline character)


#print "Reading pdbaa.nr"
#print readPdbaanr('pdbaa.nr')

print "Reading Cath Domain List"
cath_id_dict = get_cath()

print "Reading pdbaa.nr"
#readPdbaanr('pdbaa.nr', cath_id_dict)
#pdb_dict = get_pdb_dict()
writeXML("final_output.xml", readPdbaanr('pdbaa', cath_id_dict)  )
