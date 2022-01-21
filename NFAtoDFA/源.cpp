#include<iostream>
#include<vector>
#include<string>
#include<fstream>
#include<iomanip>
#include<algorithm>
using namespace std;
class MYT
{
public:
	MYT(int a, char b, int c)
	{
		beg = a;
		end = c;
		temp = b;
	}
	int beg, end;
	char temp;
private:
	friend ostream& operator<<(ostream& Out, const MYT& Obj)
	{

		Out << setw(4) << left << Obj.beg;
		Out << setw(4) << left << Obj.temp;
		Out << setw(4) << left << Obj.end;
		return Out;
	}
};

class DFA
{
public:
	char achange;
	char bchange;
	char cchange;
	vector<int>a;
	vector<int>b;
	vector<int>c;
private:
	friend ostream& operator<<(ostream& Out, const DFA& Obj)
	{

		Out << setw(4) << left << Obj.achange;
		Out << setw(4) << left << Obj.bchange;
		Out << setw(4) << left << Obj.cchange;
		return Out;
	}
};


//读文件操作
int ReadFile(string file, vector<MYT>& target)
{
	ifstream in(file);
	if (!in)
	{
		cout << "wrong" << endl;
		return -1;
	}
	int beg, end;
	char temp;
	while (in >> beg >> temp >> end)
	{
		MYT demo(beg, temp, end);
		target.push_back(demo);
	}
	in.close();
	return 1;
}

int cmp(int a, int b)
{
	return a < b;
}

//判断字符是否存在在向量
int not_in(int a, vector<int>A)
{
	for (int i = 0; i < A.size(); i++)
	{
		if (a == A[i])
		{
			return 0;
		}
	}
	return 1;
}

int not_in(vector<int>A, vector<vector<int>>AA)
{
	sort(A.begin(), A.end(),cmp);
	for (int i = 0; i < AA.size(); i++)
	{
		sort(AA[i].begin(), AA[i].end(), cmp);
		if (A == AA[i])
		{
			return 0;
		}
	}
	return 1;
}
//创建起始空串
void create_A(vector<MYT> target, vector<int>& A, int no = 0)
{
	if (not_in(no, A))
	{
		A.push_back(no);
	}
	for (int i = 0; i < target.size(); i++)
	{
		if (target[i].beg == no && target[i].temp == 'e')
		{
			create_A(target, A, target[i].end);//递归检索空串末端
		}
	}
	if (not_in(no, A))
	{
		A.push_back(no);
		return;
	}
	else
	{
		return;
	}

}


//开始子集法遍历
void findtag(char tag, vector<MYT> target, vector<int>& A, vector<int>& B)
{
	for (int i = 0; i < A.size(); i++)
	{
		for (int j = 0; j < target.size(); j++)
		{
			if (target[j].beg == A[i] && (target[j].temp == tag))
			{
				if (not_in(A[i], B))
				{
					B.push_back(target[j].end);
				}
			}
		}

	}
	vector<int> C = B;
	for (int i = 0; i < C.size(); i++)
	{
		create_A(target, B, C[i]);
	}
	sort(B.begin(), B.end(), cmp);
}


//生成最终的结果向量
void finalvector(vector<char> tag,vector<MYT> target,vector<vector<int>>& result,vector<DFA>& res)
{
	vector<int> A;
	create_A(target, A);
	result.push_back(A);
	int m_count = 0;
	int flag = 0;
	while (true)
	{
		m_count = result.size();
		vector<vector<int>> temp=result;
		for (int i = flag; i < result.size(); i++)
		{		
				
				vector<int>B,C;
				DFA tt;
				findtag('a', target, result[i], B);
				findtag('b', target, result[i], C);
				if (not_in(B,temp)&& not_in(C, temp))
				{
					temp.push_back(B);
					temp.push_back(C);
					tt.a = result[i];
					tt.b = B;
					tt.c = C;
				}
				else if (not_in(B, temp) && !not_in(C, temp))
				{

					temp.push_back(B);
					tt.a = result[i];
					tt.b = B;
					tt.c = C;
				}
				else if (!not_in(B, temp) && not_in(C, temp))
				{
					temp.push_back(C);
					tt.a = result[i];
					tt.b = B;
					tt.c = C;
				}
				else
				{

					tt.a = result[i];
					tt.b = B;
					tt.c = C;
				}
				res.push_back(tt);
				
		}
		flag = result.size();
		result = temp;
		if (m_count==result.size())
		{
			break;
		}
	}
}
//修正格式生成三元组
void create_tuple(vector<vector<int>>& result, vector<DFA>& res)
{
	for (int i = 0; i < result.size(); i++)
	{
		sort(result[i].begin(), result[i].end(), cmp);
	}
	for (int i = 0; i < res.size(); i++)
	{
		for (int j = 0; j < result.size(); j++)
		{
			if (res[i].a==result[j])
			{
				res[i].achange = 65 + j;
			}
			if (res[i].b == result[j])
			{
				res[i].bchange = 65 + j;
			}
			if (res[i].c == result[j])
			{
				res[i].cchange = 65 + j;
			}
		}
	}
}
//写操作
void OutputFile(vector<DFA>& v_tuple, string file, vector<int> a)
{
	ofstream on(file);
	for (int i = 0; i < v_tuple.size(); i++)
	{
		on << v_tuple[i] << endl;
	}
	on << "start state:";
	for (int i = 0; i < a.size(); i++)
	{
		if (a[i]==0)
		{
			on <<(char)(65 + i) << ",";
		}
	}
	on<< endl;
	on << "accepting states:";
	for (int i = 0; i < a.size(); i++)
	{
		if (a[i] == 1)
		{
			on << (char)(65 + i) << ",";
		}
	}
	on << endl;

	on.close();
}

void findstate(vector<vector<int>>& res, vector<MYT> target,vector<int>& a)
{
	int temp = target[target.size() - 1].end;
	for (int i = 0; i < res.size(); i++)
	{
		if (!not_in(temp,res[i]))
		{
			a.push_back(1);
		}
		else
		{
			
			a.push_back(0);
			
		}
	}
}

int main()
{
	vector<MYT> target;
	ReadFile("input.txt", target);
	vector<int> A, B,C,D,E;
	create_A(target, A);

	findtag('a', target, A, B);
	findtag('b', target, A, C);
	findtag('a', target, C, D);
	findtag('b', target, C, E);
	//调试结果代码
	/*for (int i = 0; i < A.size(); i++)
	{
		cout << A[i] << ",";
	}
	cout << endl;
	for (int i = 0; i < B.size(); i++)
	{
		cout << B[i] << ",";
	}
	cout << endl;
	for (int i = 0; i < C.size(); i++)
	{
		cout << C[i] << ",";
	}
	cout << endl;
	for (int i = 0; i < D.size(); i++)
	{
		cout << D[i] << ",";
	}
	cout << endl;
	for (int i = 0; i < E.size(); i++)
	{
		cout << E[i] << ",";
	}*/
	vector<vector<int>> result;
	vector<DFA>res;
	vector<int> x;
	
	vector<char> tag = { 'a','b' };
	finalvector(tag, target, result, res);
	//cout << endl;
	create_tuple(result, res);
	//for (int i = 0; i < res.size(); i++)
	//{
	//	cout << res[i].achange << ',' << res[i].bchange << ',' << res[i].cchange << ',' << endl;
	//}
	//for (int i = 0; i < result.size(); i++)
	//{
	//	for (int j = 0; j < result[i].size(); j++)
	//	{
	//		cout << result[i][j] << ',' ;
	//	}
	//	cout << endl;
	//}
	findstate(result, target, x);
	OutputFile(res, "output.txt",x);
}