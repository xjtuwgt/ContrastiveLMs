import pickle
import argparse
from tqdm import tqdm
from dataUtils.db_extractor import DocDB, get_edges, title_to_id_extractor

def hyper_link_ner_extractor(doc_db: DocDB, title_to_id: dict):
    output_data = {}
    for title, doc_id in tqdm(title_to_id.items()):
        text_with_links = pickle.loads(doc_db.get_doc_text_with_links(doc_id))
        text_ner = pickle.loads(doc_db.get_doc_ner(doc_id))
        print('ner {}\n{}'.format(len(text_ner), text_ner))
        print('text {}\n{}'.format(len(text_with_links), text_with_links))
        print('+' * 75)

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
    parser.add_argument('--db_path', type=str, default=None, required=True, help='/path/to/saved/db.db')
    args = parser.parse_args()

    doc_db = DocDB(db_path=args.db_path)
    title_to_id = title_to_id_extractor(doc_db=doc_db, row_num=5)
    hyper_link_ner_extractor(doc_db=doc_db, title_to_id=title_to_id)