import google.generativeai as genai
import json, os, datetime

# এআই কনফিগারেশন
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_long_article(cat):
    model = genai.GenerativeModel('gemini-pro')
    # ৫০০+ শব্দের জন্য প্রম্পট
    prompt = f"Write a 600-word highly detailed, verified professional blog post in Bengali about {cat}. Use points, analysis, and ensure the content is engaging. Also, provide a source name and URL at the very end. Format as JSON: title, content, source_name, source_url."
    
    response = model.generate_content(prompt)
    try:
        data = json.loads(response.text.strip('`').replace('json', ''))
        data['category'] = cat
        data['id'] = int(datetime.datetime.now().timestamp())
        return data
    except: return None

if __name__ == "__main__":
    # ট্রেন্ডিং ক্যাটাগরি
    cats = ["টেকনোলজি", "সারা বিশ্ব", "ভবিষ্যৎ বিজ্ঞান"]
    new_posts = []
    for c in cats:
        post = generate_long_article(c)
        if post: new_posts.append(post)
    
    if new_posts:
        with open('database.json', 'r+', encoding='utf-8') as f:
            db = json.load(f)
            db = new_posts + db
            f.seek(0)
            json.dump(db[:20], f, ensure_ascii=False, indent=4)
