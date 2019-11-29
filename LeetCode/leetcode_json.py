import os
import eventlet
import pandas as pd
import requests
import json

path_df_links = 'df_links_01.csv'
path_df_problems = 'df_problems_01.csv'

post_url = "https://leetcode-cn.com/graphql/"


def getQuestion(titleSlug, debug=False):
    data = {"operationName": "questionData", "variables": {"titleSlug": titleSlug},
            "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    envInfo\n    book {\n      id\n      bookName\n      pressName\n      description\n      bookImgUrl\n      pressImgUrl\n      productUrl\n      __typename\n    }\n    isSubscribed\n    __typename\n  }\n}\n"}
    sjson = json.dumps(data)

    res = requests.post(post_url, data=sjson, headers={'Content-Type': 'application/json'}).json()
    question = res['data']['question']
    # print(question)
    questionId = question['questionId']  # 问题id
    content = question['content']  # 问题内容（英）
    translatedTitle = question['translatedTitle']  # 标题（中）
    translatedContent = question['translatedContent']  # 内容（中）
    difficulty = question['difficulty']  # 难度
    likes = question['likes']  # 点赞数
    dislikes = question['dislikes']  # 不喜欢数量
    isLiked = question['isLiked']  # 是否点赞
    similarQuestions = json.loads(question['similarQuestions'])  # 相似题目
    similarQuestionTitleSlugs = [sq['titleSlug'] for sq in similarQuestions]
    topicTags = question['topicTags']  # 标签列表
    topicSlug = [topic['slug'] for topic in topicTags]  # 标签名称（英）
    topicName = [topic['translatedName'] for topic in topicTags]  # 标签名称（中）
    stats = json.loads(question['stats'])  # 通过情况
    totalAcceptedRaw = stats['totalAcceptedRaw']  # 通过数量
    totalSubmissionRaw = stats['totalSubmissionRaw']  # 提交数量
    acRate = stats['acRate']  # AC比例
    if debug:
        print(questionId, translatedTitle, difficulty, likes, dislikes, isLiked, topicSlug,
              totalAcceptedRaw, totalSubmissionRaw, acRate)
        print(similarQuestionTitleSlugs)
        print(content, translatedContent)

    df_tmp = pd.DataFrame()
    df_tmp = df_tmp.append([[
        questionId, translatedTitle, titleSlug, difficulty, likes, dislikes, topicSlug, topicName,
        totalAcceptedRaw, totalSubmissionRaw, acRate, similarQuestionTitleSlugs]])
    df_tmp.columns = ['questionId', 'translatedTitle', 'titleSlug', 'difficulty', 'likes', 'dislikes',
                      'topicSlug', 'topicName', 'totalAcceptedRaw', 'totalSubmissionRaw',
                      'acRate', 'similarQuestionTitleSlugs']
    return df_tmp


def get_all():
    if os.path.exists(path_df_problems):
        df_problems = pd.read_csv(path_df_problems)
    else:
        df_problems = pd.DataFrame()
    df_links = pd.read_csv(path_df_links)
    count_no_spider = df_links[df_links['is_crawled'] == False].shape[0]
    while count_no_spider:
        for i in range(df_links.shape[0]):
            is_crawled = df_links.loc[i, 'is_crawled']
            if is_crawled:
                continue
            title = df_links.loc[i, 'title']
            href = df_links.loc[i, 'href']
            print(href)

            with eventlet.Timeout(20, False):  # 设置超时时间为10秒
                try:
                    df_tmp = getQuestion(href.split('/')[-1])
                    df_problems = df_problems.append(df_tmp)
                    df_links.loc[i, 'is_crawled'] = True
                    print(href, 'success\n')
                except:
                    print(href, 'False\n')
                    continue

            df_problems.to_csv(path_df_problems, index=False, encoding='utf8')
            df_links.to_csv(path_df_links, index=False, encoding='utf8')
            count_no_spider = df_links[df_links['is_crawled'] == False].shape[0]


if __name__ == '__main__':
    is_debug = False
    if is_debug:
        titleSlug = "two-sum"
        getQuestion(titleSlug, debug=True)
    else:
        get_all()
