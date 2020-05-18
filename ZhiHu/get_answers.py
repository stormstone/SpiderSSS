import json
import os
import re
import time

import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
question_answers_api = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={}&offset={}&sort_by=default"


def get_answers_by_question_id(question_id, limit=5, offset=0, base_output='question_answers/'):
    output = base_output + str(question_id) + '/'
    if not os.path.exists(output):
        os.makedirs(output)

    is_end = False
    while not is_end:
        print('question:', question_id, '\t offset:', offset)
        response = requests.get(question_answers_api.format(question_id, limit, offset), headers=headers)
        with open(output + str(offset) + '.json', mode='w', encoding='utf8') as f:
            f.write(response.text)
        offset += limit
        is_end = json.loads(response.text).get('paging').get('is_end')
        time.sleep(10)


def get_contend_by_question_id(question_id, base_output='question_answers/'):
    json_dir = base_output + str(question_id) + '/'
    lst_jsons = os.listdir(json_dir)
    regex = re.compile("<.*?>|\n|\t")
    df_answers = pd.DataFrame()
    for json_file in lst_jsons:
        if json_file.split('.')[-1] != 'json':
            continue
        print(json_file)
        with open(json_dir + json_file, 'r', encoding='utf8') as f:
            jsonData = json.load(f).get('data')
        for itemData in jsonData:
            df_tmp = pd.DataFrame()
            df_tmp['answer_id'] = [itemData['id']]
            df_tmp['question_id'] = [question_id]
            df_tmp['author_url_token'] = [itemData['author']['url_token']]
            df_tmp['author_name'] = [itemData['author']['name']]
            df_tmp['voteup_count'] = [itemData['voteup_count']]
            df_tmp['comment_count'] = [itemData['comment_count']]
            df_tmp['content'] = ["".join(re.sub(regex, "", itemData['content']))]
            print(df_tmp)
            df_answers = df_answers.append(df_tmp)
    df_answers.to_csv(json_dir + str(question_id) + '.csv', index=False)


if __name__ == '__main__':
    # get_answers_by_question_id(31770703, 20)
    get_contend_by_question_id(23077814)
