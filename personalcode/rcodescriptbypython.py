

category=['Design',
    'FilmandVideo',
    'Food',
    'Games',
    'Publishing',
    'Music',
    'Fashion',
    'Theater',
    'Photography',
    'Art',
    'Comics',
    'Technology',
    'Crafts',
    'Journalism',
    'Dance']

code= '/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarter_dataset/data/empirical_test_data/logistic/code.txt'
with open(code,'w') as f:


    for x in category:
        locals()['%s'%x]='''logit%s.model <- glm(project_state_code ~
                            creator_has_backed__projects_number+
                            creator_has_built_projects_number+
                            duration+
                            goal_usd+
                            Gini_coef+
                            backers_count+
                            creator_friends_facebook_number+
                            has_a_video_d+
                            updates_number+
                            comments_count
                            ,family=binomial, data=%s)
                            '''%(x,x)
        f.write(locals()['%s'%x] + '\n')
    f.write('\n')
    for x in category:
        a='summary(logit%s.model)'%x
        f.write(a+'\n')
    f.write('\n')
    for x in category:
        b='write.csv(summary(logit%s.model),file="/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarter_dataset/data/empirical_test_data/logistic/%s.csv")'%(x,x)
        f.write(b+'\n')
    f.write('\n')
    for x in category:
        c="print ('-----------------------')"
        c_a="print ('state of %s')"%x
        c_b='summary(%s)'%x
        f.write(c+'\n'+c_a+'\n'+c_b+'\n')
