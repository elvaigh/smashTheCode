#define _CRT_SECURE_NO_WARNINGS 
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <deque>
#include <map>
#include <ctime>

#include <fstream>


int depth = 5;
int dirX[] = { -1,0,0,1 };
int dirY[] = { 0,-1,1,0 };

using namespace std;
vector<char> mapp(72, '@');

deque<char> nextinput;
int next_column;
void updateNode(const vector<char>& deque, const char& couleur, const int& nextpos, vector<int>& foo)
{
	for (int i(0); i < 4; i++)
	{
		int u = nextpos / 6;
		int v = nextpos - 6 * u;
		u += dirX[i];
		v += dirY[i];
		int newpos = u * 6 + v;

		if (u >= 0 && u <= 11 && v >= 0 && v <= 5)
		{
			char bf = deque[newpos];
			int w = (bf - 'B') / 5;
			if ((couleur - 'B' == bf - 'B' - 5 * w || bf == 'A') && find(foo.begin(), foo.end(), newpos) == foo.end())
			{
				foo.push_back(newpos);
				if (bf != 'A')
					updateNode(deque, couleur, newpos, foo);
			}
		}
	}
}

//!
//! \brief Find all bloc of the same color in the neighborhood of pos
//!
//! \param : k : the color of the new element at pos
//! \param : pos : the pos of the element
//! \param : foo : a vector to keep track of position of all block of the same color
//! \return :int : return the score for the updatePosition
//!
int updatePosition(vector<char>& deque, const char& k, const int& pos, vector<int>& foo)
{
	foo.push_back(pos);

	for (int i(0); i < 3; i++)
	{
		int u = pos / 6;
		int v = pos - 6 * u;
		u += dirX[i];
		v += dirY[i];
		if (u >= 0 && u <= 11 && v >= 0 && v <= 5)
		{
			char bf = deque[u * 6 + v];
			if (bf != '@') {
				int w = (bf - 'B') / 5;
				if ((k - 'B' == bf - 'B' - 5 * w || bf == 'A') && find(foo.begin(), foo.end(), u * 6 + v) == foo.end())
				{
					foo.push_back(u * 6 + v);
					if (bf != 'A')
						updateNode(deque, k, u * 6 + v, foo);
				}
			}
		}
	}
	int score = foo.size();
	for_each(begin(foo), end(foo), [&deque, &k, &score](const int& x) {
		if (deque[x] != 'A')
			deque[x] = 'B' + (score - 1) * 5 + k - 'B';
	});
	return score;
}

void dropp(vector<char>& deque, int x)
{
	deque[x] = '@';
	while (x < 72) {
		deque[x] = (x + 6 > 71 ? '@' : deque[x + 6]);
		x += 6;
	}
}


void clear(vector<char>& deque, vector<int> &foo)
{
	sort(foo.begin(), foo.end(), [](const int& a, const int& b)
	{
		auto aa = a / 6;
		auto bb = b / 6;
		if (aa > bb)
			return true;
		else if (aa == bb && a - 6 * aa > b - 6 * bb)
			return true;
		else
			return false;
	});

	for_each(foo.begin(), foo.end(),
		[&deque](const int& x)
	{
		dropp(deque, x);
	});
}

inline int taille(const vector<int>& foo, const vector<char>& deque)
{
	int n(0);
	for_each(foo.begin(), foo.end(), [&n, &deque](const int& x)
	{
		if (deque[x] != 'A')
			n++;
	});
	return n;
}

//!
//! \brief
//!
//! \param : j 
//! \param : i 
//! \return :int
//!
bool ajouterPiece(vector<char>& deque, const int& j, const int& i, int &score, vector<int>& foo)
{
	int k(0);
	while (k < 12 && deque[j + k * 6] != '@')
		k++;
	if (k > 10)
		return false; // Impossible to add
	char a, b;
	a = deque[j + k * 6] = nextinput[2 * i];

	int r = updatePosition(deque, a, j + k * 6, foo);
	b = nextinput[2 * i + 1];
	bool joue = false;
	if (taille(foo, deque) >= 3)
	{
		if (a == b) {
			joue = true;
			foo.push_back(j + (k + 1) * 6);
		}
		if (taille(foo, deque) > 3) {
			clear(deque, foo);
			score = foo.size();
		}
	}
	if (!joue) {
		deque[j + (++k) * 6] = b;
		foo.clear();
		int s = updatePosition(deque, b, j + k * 6, foo);
		if (taille(foo, deque) > 3) {
			clear(deque, foo);
			score += foo.size();
		}
	}
	// Return the first block added
	return true;
}


void updateMap(vector<char>& deque,int &score)
{
	vector<int> visite(72, false);
	int i(0);
	while(i < 72)
	{
		vector<int> foo;
		if (deque[i] != 'A' && deque[i] != '@' && visite[i] == false)
		{
			int bf = (deque[i] - 'B') / 5;
			char k = deque[i] - 5 * bf;
			updateNode(deque, k, i, foo);
			if (taille(foo,deque) > 3)
			{
				clear(deque,foo);
				score += 2 * foo.size(); // COMBO !!!
				i--;
			}
			else
			{
				for_each(foo.begin(), foo.end(), [&visite,&foo](const int& x)
				{
					visite[x] = true;
				});
			}
		}
		i++;
	}
}

vector<char> bestDeque;

//!
//! \brief
//!
//! \param : deque 
//! \param : i 
//! \param : score 
//! \return :int
//!
int play(vector<char>& deque = mapp, const int& i = 0, int score = 0)
{
	if (i == depth)
		return score;

	int min = -1000, localscore, bestcolumn = 0;

	for (int j(0); j < 6; j++)
	{
		localscore = 0;
		vector<char> previousDeque = deque;
		vector<int> foo;
		if (ajouterPiece(deque, j, i, localscore, foo))
		{
			if (localscore > 3)
			{
				updateMap(deque,localscore);
				// update map en incrementing score
			}

			int res = play(deque, i + 1, score + localscore);

			if (res > min)
			{
				min = res;
				bestcolumn = j;
				if (i == 0)
					bestDeque = deque;
			}
		}
		deque = previousDeque;
	}
	if (i == 0)
	{
		next_column = bestcolumn;
		mapp = bestDeque;
	}
	return min;
}



void output()
{
	for (int i = 11; i > -1; i--) {
		{
			for (int j(0); j < 6; j++)
				cerr << mapp.at(j + i * 6) << " ";
		}
		cerr << endl;
	}
}

void readInput(const int& k)
{
	for (int i(0); i < 8; i++)
	{
		char color1, color2;
		cin >> color1 >> color2;
		color1 += 17;
		color2 += 17;

		if (!k) {
			nextinput.push_back(color1);
			nextinput.push_back(color2);
		}
		else if (i == 7) {
			nextinput.pop_front(); nextinput.pop_front();
			nextinput.push_back(color1); nextinput.push_back(color2);
		}
	}
	for (int i = 11; i > -1; i--) {
		string row;
		cin >> row;
		for (int j(0); j < row.size(); j++)
		{
			if (row.at(j) == '0') {

				mapp[i * 6 + j] = 'A';
			}
		}
	}
	for (int i = 0; i < 12; i++) {
		string row; // One line of the map ('.' = empty, '0' = skull block, '1' to '5' = colored block)
		cin >> row; cin.ignore();
	}
	//output();
}

void generateGame()
{
	ofstream flux("test");
	vector<pair<int, int> > vecteur;
	for (int i(0); i < 200; i++)
	{
		int n = rand() % 5 + 1;
		vecteur.push_back(make_pair(n, n));
	}
	for (int i(0); i < 200 - 8; i++)
	{
		for (int j(i); j < i + 8; j++)
		{
			flux << vecteur.at(j).first << " " << vecteur.at(j).second << " ";
		}
		flux << endl;
	}
	flux.close();
}
int main()
{
	srand(time(NULL));
	// generateGame();
	int u = 40;
	// std::freopen("test", "r", stdin);	
	// game loop
	int i(0);
	while (1) {
		readInput(i);
		play();
		output();
		i++;
		cout << next_column << endl; // "x": the column in which to drop your blocks
	}
}