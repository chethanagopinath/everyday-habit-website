# lets just do the LC portion or 3 todos for now during the weekend
from flask import Flask
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route("/todo", methods=["POST"])
def add_todo():
    pass

@app.route("/leetcode_stats", methods=["GET"])
def get_leetcode_stats():
    pass

@app.route("/leetcode_problem", methods=["GET"])
def get_leetcode_problem_based_on_tag():
    data = {"operationName":"questionData","variables":{"titleSlug":"two-sum"},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

    r = requests.post('https://leetcode.com/graphql', json = data).json()
    soup = bs(r['data']['question']['content'], "html.parser")
    title = r['data']['question']['title']
    question =  soup.get_text().replace('\n',' ')

    print(data)

    return {
        "title": title,
        "question": question
    }


@app.route("/everyday_lc_problem", methods=["GET"])
def get_everyday_question():
    data = {
            "operationName": "questionOfToday",
            "variables": {},
            "query": "query questionOfToday {\n  activeDailyCodingChallengeQuestion {\n    date\n    userStatus\n    link\n    question {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      hasVideoSolution\n      hasSolution\n      topicTags {\n        name\n        id\n        slug\n      }\n    }\n  }\n}\n    "
        }
    
    #get the queries by operationName after doing a network request and seeing 
    r = requests.post('https://leetcode.com/graphql', json = data).json()

    question_link = f"https://leetcode.com{r['data']['activeDailyCodingChallengeQuestion']['link']}"
    question = r["data"]["activeDailyCodingChallengeQuestion"]["question"]
    question_tags = [tag["name"] for tag in question["topicTags"]]

    return {
        "question_link": question_link,
        "question_title": question["title"],
        "question_difficulty": question["difficulty"],
        "question_tags": question_tags
    }

@app.route("/leetcode_problem", methods=["POST"])
def save_leetcode_problem_status():
    pass

if __name__=="__main__":
    app.run(debug=True)