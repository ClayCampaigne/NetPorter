# NetPorter
NetPorter: A Social Network Migration Manager

NetPorter is an open-source project designed to facilitate the seamless transition of user follow networks between social media platforms. Initially targeting Twitter because of Elon Musk's erratic behavior and shameful ban of Substack on April 7 2023, NetPorter aims to be a general platform capable of exporting your network from a source platform so that it can be automatically tracked and kept up to date on a target platform, such as Substack Notes or Mastadon. 

We assume that exporting a user's follows from Twitter is relatively straightforward, and doesn't require authentication by the user. However, to complete the export process to another network, it is neceesary to verify the ownership of *followed* accounts, so that the user can automatically follow the correct accounts on the target platform, rather than impostors. Therefore we need to verify that the NetPorter user actually owns the respective Twitter account(s).

We envision two processes for source platform (Twitter) ownership verification. The fist is the traditional OAuth approach that any old Twitter-linked app would use. However, since Elon can be a bit petty and tyrannical, we also envision a backup "manual" method method that asks the Twitter Account owner to tweet a code that the NetPorter service randomly generates. The manual verification method would hopefully work even if the access to the Twitter APIs is rescinded, by traditional web-scraping means.
