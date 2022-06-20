//===============?g=============================================================
// Name        : NDSS2014_openVersion.cpp
// Author      : Bowlong
// Version     : NDSS2014 openVersion
// Copyright   : Copyright @2016 All rights reserved by Bowlong
// Description : C++98
//============================================================================

#include <iostream>
#include <fstream>
#include<set>
#include<vector>
#include <string>
using namespace std;

#define OUT_ALL 0////1: ouput all guess; 0: only output result
//#define GUESS_THRESHOLD 100

string padSeq[16] = { "qwer", "asdf", "1234", "1qaz", "2wsx", "3edc", "qwe",
                      "wer", "asd", "sdf", "1qa", "2ws", "3ed", "qaz", "wsx", "edc" };
string symbol = "~`!@#$%^&*()-_=+{}[]\\|;:'\"<>,.?/";
string gram[15] = { "08", "01", "07", "23", "06", "09", "12", "05", "123",
                    "087", "007", "083", "084", "089", "086" };
vector<string> guess;
set<string> dict;

int crack_num[10000];
int cnt = 0;

string newpsw;
bool Deletion(string old_psw, string new_psw) {
	
    string no_num, no_sym, no_upper, no_lower;
    int len = old_psw.length();
    for (int i = 0; i < len; i++) {
        char c = old_psw[i];
        if (c >= '0' && c <= '9') {
            no_sym += c;
            no_upper += c;
            no_lower += c;
        } else if (c >= 'a' && c <= 'z') {
            no_num += c;
            no_sym += c;
            no_upper += c;
        } else if (c >= 'A' && c <= 'Z') {
            no_num += c;
            no_sym += c;
            no_lower += c;
        } else {
            no_num += c;
            no_upper += c;
            no_lower += c;
        }
    }
    cnt++;
    guess.push_back(no_num);
    if (no_num == new_psw) {
        crack_num[cnt]++;
        return 1;
    }
    cnt++;
    guess.push_back(no_sym);
    if (no_sym == new_psw) {
        crack_num[cnt]++;
        return 1;
    }
    cnt++;
    guess.push_back(no_upper);
    if (no_upper== new_psw) {
        crack_num[cnt]++;
        return 1;
    }
    cnt++;
    guess.push_back(no_lower);
    if (no_lower == new_psw) {
        crack_num[cnt]++;
        return 1;
    }
    for (int i = 1; i < len; i++) {
        cnt++;
       
        guess.push_back(old_psw.substr(i, len - i));
        if (old_psw.substr(i, len - i) == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
        cnt++;
        guess.push_back(old_psw.substr(0, len - i));
        if (old_psw.substr(0, len - i) == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
        if (len > 2 * i) {
            cnt++;
            guess.push_back(old_psw.substr(i, len - 2 * i));
            if (old_psw.substr(i, len - 2 * i) == new_psw) {
                crack_num[cnt]++;
                return 1;
            }
        }
    }
    return 0;
}

bool Capital(string old_psw, string new_psw) {
    int len = old_psw.length();
    string tmp = old_psw;
    for (int i = 0; i < len; i++) {
        if (tmp[i] >= 'a' && tmp[i] <= 'z')
            tmp[i] -= 32;
        cnt++;
        guess.push_back(tmp);
        if (tmp == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
    }
    tmp = old_psw;
    for (int i = len - 1; i >= 0; i--) {
        if (tmp[i] >= 'a' && tmp[i] <= 'z')
            tmp[i] -= 32;
        cnt++;
        guess.push_back(tmp);
        if (tmp == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
    }

    return 0;
}

bool Reverse(string old_psw, string new_psw) {
    string tmp = old_psw;
    int len = old_psw.length();
    for (int i = 0; i < len; i++)
        tmp[i] = old_psw[len - i - 1];
    cnt++;
    guess.push_back(tmp);
    if (tmp == new_psw) {
        crack_num[cnt]++;
        return 1;
    }
    return 0;
}

bool Leet(string old_psw, string new_psw, int st) {
    int len = old_psw.length();
    cnt++;
    guess.push_back(old_psw);
    if (old_psw == new_psw) {
        crack_num[cnt]++;
        return 1;
    }
    for (int i = st; i < len; i++) {
        char c = old_psw[i];
        string tmp = old_psw;
        if (c == '0')
            tmp[i] = 'o';
        else if (c == 'o')
            tmp[i] = '0';
        else if (c == 'a')
            tmp[i] = '@';
        else if (c == '@')
            tmp[i] = 'a';
        else if (c == 's')
            tmp[i] = '$';
        else if (c == '$')
            tmp[i] = 's';
        else if (c == '7')
            tmp[i] = 't';
        else if (c == 't')
            tmp[i] = '7';
        else if (c == '3')
            tmp[i] = 'e';
        else if (c == 'e')
            tmp[i] = '3';
        else if (c == '1')
            tmp[i] = 'i';
        else if (c == 'i')
            tmp[i] = '1';

        if (tmp != old_psw) {
            if (Leet(tmp, new_psw, i + 1)) {
                crack_num[cnt]++;
                return 1;
            }
        }
    }

    return 0;
}

bool Insertion(string old_psw, string new_psw) {
    string tmp = old_psw;
    int len = old_psw.length();
    int symlen=symbol.length();
    for (int i = 0; i < 10; i++) {
        char c = '0' + i;
        tmp = old_psw + c;
        cnt++;
        guess.push_back(tmp);
        if (tmp == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
        tmp = c + old_psw;
        cnt++;
        guess.push_back(tmp);
        if (tmp == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
    }

    for (int i = 0; i < symlen; i++) {
        tmp = old_psw + symbol[i];
        cnt++;
        guess.push_back(tmp);
        if (tmp == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
        tmp = symbol[i] + old_psw;
        cnt++;
        guess.push_back(tmp);
        if (tmp == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
    }

    bool type[4] = { 0 };//num,sym,up,low
    for (int i = 0; i < len; i++) {
        char c = old_psw[i];
        if (c >= '0' && c <= '9')
            type[0] = true;
        else if (c >= 'a' && c <= 'z')
            type[3] = true;
        else if (c >= 'A' && c <= 'Z')
            type[2] = true;
        else
            type[1] = true;
    }
    if (!type[0]) {
        for (int i = 0; i < len; i++) {
            for (int j = 0; j < 10; j++) {
                tmp = old_psw;
                char c = '0' + j;
                tmp.insert(i, 1, c);
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
            }

        }
    }
    if (!type[1]) {
        int symlen = symbol.length();
        for (int i = 0; i < len; i++) {
            for (int j = 0; j < symlen; j++) {
                tmp = old_psw;
                char c = symbol[j];
                tmp.insert(i, 1, c);
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
            }
        }
    }
    if (!type[2]) {
        for (int i = 0; i < len; i++) {
            for (int j = 0; j < 26; j++) {
                tmp = old_psw;
                char c = 'A' + j;
                tmp.insert(i, 1, c);
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
            }
        }
    }
    if (!type[3]) {
        for (int i = 0; i < len; i++) {
            for (int j = 0; j < 26; j++) {
                tmp = old_psw;
                char c = 'a' + j;
                tmp.insert(i, 1, c);
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
            }
        }
    }
    for (int i = 0; i < 15; i++) {
        tmp = old_psw + gram[i];
        cnt++;
        guess.push_back(tmp);
        if (tmp == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
        tmp = gram[i] + old_psw;
        cnt++;
        guess.push_back(tmp);
        if (tmp == new_psw) {
            crack_num[cnt]++;
            return 1;
        }
    }

    return 0;
}

bool Sequencial(string old_psw, string new_psw) {
    for (int i = 0; i < 16; i++) {
        string tmp = old_psw;

        int pos = old_psw.find(padSeq[i]);
		
        if (pos != string::npos) {
            if (padSeq[i] == "qwer") {
                tmp.insert(pos + 3, 1, 't');
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
                tmp = old_psw;
                tmp.replace(pos, 4, "1234");
                cnt++;
                guess.push_back(tmp);
                if (tmp== new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
                tmp = old_psw;
                tmp.replace(pos, 4, "1qaz");
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
            } else if (padSeq[i] == "asdf") {
                tmp.insert(pos + 3, 1, 'g');
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
                tmp = old_psw;
                tmp.replace(pos, 4, "1234");
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
                tmp = old_psw;
                tmp.replace(pos, 4, "zxcv");
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
            } else if (padSeq[i] == "qwe") {
                tmp.insert(pos + 2, 1, 'r');
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
                tmp = old_psw;
                tmp.replace(pos, 3, "qaz");
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
                tmp = old_psw;
                tmp.replace(pos, 3, "asd");
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
            } else if (padSeq[i] == "asd") {
                tmp.insert(pos + 2, 1, 'f');
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
                tmp = old_psw;
                tmp.replace(pos, 3, "wsx");
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
                tmp = old_psw;
                tmp.replace(pos, 3, "qwe");
                cnt++;
                guess.push_back(tmp);
                if (tmp == new_psw) {
                    crack_num[cnt]++;
                    return 1;
                }
            }

        }
    }
    return 0;
}

bool Subword(string old_psw, string new_psw) {
    int len = old_psw.length();
    string rtn = old_psw;
    string word = "";
    bool flag = 0;
    for (int i = len - 1; i >= 0; i--) {
        char c = old_psw[i];
        if (c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z') {
            if (c >= 'A' && c <= 'Z')
                c += 32;
            string tmp = c + word;
            if (dict.find(tmp) == dict.end()) {
                if (flag == 0) {
                    word = tmp;
                } else {
                    if (rtn[i + 1] >= 'a' && rtn[i + 1] <= 'z')
                        rtn[i + 1] -= 32;
                    flag = 0;
                    word = c;
                }
            } else {
                flag = 1;
                word = tmp;
            }
        } else {
            if (flag == 1) {
                if (rtn[i + 1] >= 'a' && rtn[i + 1] <= 'z')
                    rtn[i + 1] -= 32;
                flag = 0;
            }
            word = "";
        }

    }
    if (flag == 1) {
        if (rtn[0] >= 'a' && rtn[0] <= 'z')
            rtn[0] -= 32;
    }
    cnt++;
    guess.push_back(rtn);
    if (rtn == new_psw) {
        crack_num[cnt]++;
        return 1;
    }

    return 0;
}

bool genGuess(string old_psw, string new_psw) {
    cnt = 1;
    if (old_psw == new_psw) {
        crack_num[1]++;
        return 1;
    }

    int len = old_psw.length();
    if (Sequencial(old_psw, new_psw))
        return 1;
    //delete
    if (len > 6 && Deletion(old_psw, new_psw))
        {   return 1;}
    //insert
    if (len < 10 && Insertion(old_psw, new_psw))
        return 1;
    //capital
    if (Capital(old_psw, new_psw))
        return 1;
    if (Reverse(old_psw, new_psw))
        return 1;
    if (Leet(old_psw, new_psw, 0))
        return 1;
    if (Subword(old_psw, new_psw))
        return 1;

    return 0;
}

int main(int argc, char * argv[]) {
    string line;
    //printf("here");
    if (argc < 2) {
        printf("USAGE: %s <test_file> <GUESSES>\n", argv[0]);
        return 1;
    }
    
    int GUESS_THRESHOLD = stoi(argv[2]);
    //printf("Reading %s\n", argv[1]);
    ifstream fin(argv[1]);
    ofstream fout("guesses_das.et.al.tsv");
    ifstream din("english.txt");


    while (getline(din, line)) {
        dict.insert(line);
    }

    int crack = 0, total = 0, same = 0;
    int ll = 0;
    while (getline(fin, line)) {
        ll++;
        total++;
	//	if (ll>1000)continue;
        int len = line.length();
        string old_psw, new_psw, mail;
        string inf[7];
        int st = 0, tmp = 0;
        if (line[len-1] == '\r') {
            line = line.substr(0, len-1);
            len --;
        }
                        
        for (int i = 0; i < len; i++) {
            if (line[i] == '\t') {
                inf[tmp++] = line.substr(st, i - st);
                st = i + 1;
            }
        }
        inf[tmp++] = line.substr(st, len - st);

        mail = inf[0];
        old_psw = inf[1];
        new_psw = inf[2];
        /// cout<<"InPassword: \t" << old_psw << "\t" << new_psw;
        newpsw = new_psw;
        if (old_psw == new_psw)
            same++;
        //cout << "In main: " << total << ' ' << old_psw << ' ' << new_psw << " " << endl;
         if (ll!=1)
             fout<<endl;
         fout << line << endl;
        bool tt = genGuess(old_psw, new_psw);
        //cout<<"tt"<<tt;
        int gnum = 0;
        if (OUT_ALL)
            fout << old_psw << "\t";
        for (vector<string>::iterator i = guess.begin(); i != guess.end(); i++) {
            if (!i->empty() && *i != old_psw) {
                gnum++;
                if (OUT_ALL)
                    fout << *i << "\t";
                if (gnum > GUESS_THRESHOLD-1)
                    break;
            }
        }
        fout << endl;
        if (tt) {
            crack++;
             fout << "cracked: " << crack << endl;
          //  cout << "crack " << crack << endl;
        }
        else fout<<"failed"<<endl;
        guess.clear();
    }
    //cout << "guess num\tcrack num\n";
    int sum = 0;
    for (int i = 1; i <= GUESS_THRESHOLD; i++) {
        sum += crack_num[i];
        //cout << i << '\t' << sum << endl;
    }
    cout <<"n = "<< GUESS_THRESHOLD << '\t'<<" Accuracy = " << (sum*100.0)/total << endl;
    //cout << "total crack: " << crack << '/' << total << endl;

    return 0;
}
