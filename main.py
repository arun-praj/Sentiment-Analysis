import preprocesser as pp

if __name__ == "__main__":
    tweet = "Hiiiiiiii, i'm @_aaarun and I just lunched https://www.facebook.com !!!!!!.😇. #newsite #newwworld"
    print(pp.cleaner(tweet))
    # print(help(pp.preprocess_string))

# regex =  re.compile('[%s]' % re.escape(string.punctuation))
#     processed_string = regex.sub('',processed_string)