from lxml import html
import requests
import time
with open('na_records.tsv', 'w', encoding="utf8") as output:    
    for i in range(1, 273):
        if i == 60 or i == 103:
            continue
        print("Processing: NA %d"%i)
        url = "https://www.ecp.gov.pk/ConstResult.aspx?Const_Id=NA-" + str(i) + "&type=NA&Election_ID=10070&Election=GENERAL%20ELECTION%2025%20JUL%202018"
        page = requests.get(url)
        tree = html.fromstring(page.content)
        rej_votes_arr = tree.xpath('//span[@id="ContentPlaceHolder1_lblRejVotes"]/text()')
        total_votes_arr = tree.xpath('//span[@id="ContentPlaceHolder1_lblVotesPolled"]/text()')
        voters_registered_arr = tree.xpath('//span[@id="ContentPlaceHolder1_lblRegVoters"]/text()')
        if len(rej_votes_arr) != 0 and len(total_votes_arr) != 0 and len(voters_registered_arr) != 0:
            rej_votes = int(rej_votes_arr[0])
            total_votes = int(total_votes_arr[0])
            voters_registered = int(voters_registered_arr[0])

            winner_arr = tree.xpath('//tr[@class="tr3"]//td//p/text()')
            if len(winner_arr) != 0:
                win_name, win_party, win_votes_str = winner_arr
                win_votes = int(win_votes_str)
                runner_up_arr = tree.xpath('//tr[@class="tr1"]//td//p/text()')
                votes = [int(x) for i,x in enumerate(runner_up_arr) if (i + 1) % 3 == 0]
                votes = sorted(votes, reverse=True)
                output.write("NA%d\t%d\t%d\t%d\t%f"%(i,voters_registered,rej_votes, total_votes, 100 * float(rej_votes)/ float(total_votes)))
                output.write("\t%d\t%d\t%d\t%s\n"%(win_votes, votes[0], (win_votes - votes[0]),win_party))
