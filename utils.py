""" Utility functions for abstracts project"""

import urllib.request as ul


def get_abstracts_txt(year='2017',month='01'):
    """ Downloads the abstracts data from abstract service and saves it to text file"""
    
    url = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&author=&object=&start_mon={1}&start_year={0}&end_mon={1}&end_year={0}&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=3000&start_nr=1&jou_pick=NO&ref_stems=&data_and=YES&abstract=YES&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&data_type=PLAINTEXT&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1".format(year,month) 
    
    f = ul.urlopen(url)
    txt = f.read().decode("latin1")

    fname = 'data/abstracts_{}_{}.txt'.format(year,month) 
    with open(fname,'w') as fil:
        fil.write(txt)
    print("Done download for year {} month {}".format(year,month))
    return

def br2spc(str):
    """ Replaces \n with space and strips spaces from start and end."""
    return str.replace("\n",' ').strip(' ')

def get_record(p,k1,k2):
    """ Returns string between k1 and k2 in the text p"""
    try:
        return br2spc(p.split(k1)[1].split(k2)[0]).replace('                      ',' ')
    except:
        return ''


def get_pubs_dict(
    fnames = ['data/abstracts_2017_01.txt', 'data/abstracts_2017_02.txt', 'data/abstracts_2017_03.txt', 'data/abstracts_2017_04.txt', 'data/abstracts_2017_05.txt', 'data/abstracts_2017_06.txt', 'data/abstracts_2017_07.txt', 'data/abstracts_2017_08.txt', 'data/abstracts_2017_09.txt', 'data/abstracts_2017_10.txt', 'data/abstracts_2017_11.txt', 'data/abstracts_2017_12.txt']
    ):

    """ 
        Returns the dictionary of publications from the text files in the fnames list.
    """

    pubs_dict = {}
    all_abstracts = []
    
    for fname in fnames:
        with open(fname,'r') as f:
            txt = f.read()
    

        pubs = txt.split("Title:")[1:]
        for p in pubs:
    
            try:
                pub = {}
                title =       get_record(p,'              ',"Authors:")
                authors =     get_record(p,"Authors:",'Affiliation:')
                aff =         get_record(p,"Affiliation:",'Publication:')
                publication = get_record(p,"Publication:",'Publication Date:')
                journal = publication.split(',')[0]
                pub_date =    get_record(p,"Publication Date:",'Origin:')
                origin =      get_record(p,'Origin:',"Keywords:")
                keys =        get_record(p,"Keywords:",'Abstract Copyright:')
                bibcode =     get_record(p,'Bibliographic Code:','Abstract')
                try:
                    abs = br2spc(p.split("Abstract")[-1])
                except:
                    abs = ''
      
#                pub['title'] = title
#                pub['authors'] = authors
#                pub['bibcode'] = authors
                pub['journal'] = journal        
                pub['abstract'] = abs
                pubs_dict[bibcode] = pub
                all_abstracts.append(abs)
            except Exception as e:
                print(e)
#            print(p)
    
    return pubs_dict, "".join(all_abstracts)
