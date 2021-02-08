from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle
import argparse
from dataUtils.db_extractor import DocDB, get_edges, title_to_id_extractor

def hyper_link_ner_extractor(doc_db: DocDB, title_to_id: dict):
    output_data = {}
    doc_ids = doc_db.get_doc_ids()
    for doc_id in doc_ids:
        title = doc_db.get_doc_title(doc_id)
        text_with_links = pickle.loads(doc_db.get_doc_text_with_links(doc_id))
        text_ner = pickle.loads(doc_db.get_doc_ner(doc_id))

        hyperlink_titles, hyperlink_spans = [], []
        hyperlink_paras = []
        for i, sentence in enumerate(text_with_links):
            _lt, _ls, _lp = [], [], []
            t = get_edges(sentence)
            if len(t) > 0:
                for link_title, mention_entity in t:
                    if link_title in title_to_id:
                        _lt.append(link_title)
                        _ls.append(mention_entity)
                        doc_text = pickle.loads(doc_db.get_doc_text(title_to_id[link_title]))
                        _lp.append(doc_text)

            hyperlink_titles.append(_lt)
            hyperlink_spans.append(_ls)
            hyperlink_paras.append(_lp)

        output_data[title] = {'hyperlink_titles': hyperlink_titles,
                              'hyperlink_paras': hyperlink_paras,
                              'hyperlink_spans': hyperlink_spans,
                              'text_ner': text_ner}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('db_path', type=str, help='/path/to/saved/db.db')
    args = parser.parse_args()
    for key, value in vars(args).items():
        print(key, value)

    db_path = args.db_path
    doc_db = DocDB(db_path=db_path)
    title_to_id = title_to_id_extractor(doc_db=doc_db)