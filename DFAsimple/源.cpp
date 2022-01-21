#include<iostream>
#include<vector>
#include<string>
#include<fstream>
#include<iomanip>
using namespace std;

class Res
{
public:
	int a;
	char b;
	int c;

private:
	friend ostream& operator<<(ostream& Out, const Res& Obj)
	{

		Out << setw(4) << left << Obj.a;
		Out << setw(4) << left << Obj.b;
		Out << setw(4) << left << Obj.c;
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

//读取文件并且获得开始状态集合和接受状态集合
int ReadFile(string file, vector<DFA>& target, vector<char>& m_start,vector<char>& m_accept )
{
	ifstream in(file);
	vector<string> demo;
	if (!in)
	{
		cout << "wrong" << endl;
		return -1;
	}
	char e, a, b;
	while (in >> e >> a >> b)
	{
		DFA temp;
		temp.achange = e;
		temp.bchange = a;
		temp.cchange = b;
		target.push_back(temp);
	}
	in.close();
	ifstream in1(file);
	string m_state;
	while (in1>>m_state)
	{
		demo.push_back(m_state);
	}
	string str1,str2,st,acc;
	str1 = demo[demo.size() - 3];
	str2 = demo[demo.size() - 1];
	st = str1.substr(str1.find(':') + 1);
	acc= str2.substr(str2.find(':') + 1);
	//cout << str1 << endl << str2 << endl << st << endl << acc << endl;
	for (int i = 0; i < st.size(); i++)
	{
		if (st[i]!=',')
		{
			m_start.push_back(st[i]);
		}
	}
	for (int i = 0; i < acc.size(); i++)
	{
		if (acc[i] != ',')
		{
			m_accept.push_back(acc[i]);
		}
	}
	in1.close();
	return 1;
}
//判断字符是否存在在向量中
int is_in(char a,vector<char> b)
{
	for (int i = 0; i < b.size(); i++)
	{
		if (a==b[i])
		{
			return 1;
		}
	}
	return 0;
}
//得到状态经过a边的状态
char find_a_tag(char a,vector<DFA> target)
{
	for (int i = 0; i < target.size(); i++)
	{
		if (a==target[i].achange)
		{
			return target[i].bchange;
		}
	}
}
//得到状态组经过a边得到的状态
char find_va_tag(vector<char> a, vector<DFA> target)
{
	for (int i = 0; i < target.size(); i++)
	{
		if (a[0] == target[i].achange)
		{
			return target[i].bchange;
		}
	}
}

//得到状态经过b边得到的状态
char find_b_tag(char a, vector<DFA> target)
{
	for (int i = 0; i < target.size(); i++)
	{
		if (a == target[i].achange)
		{
			return target[i].cchange;
		}
	}
}
//得到状态组经过b边得到的状态
char find_vb_tag(vector<char> a, vector<DFA> target)
{
	for (int i = 0; i < target.size(); i++)
	{
		if (a[0] == target[i].achange)
		{
			return target[i].cchange;
		}
	}
}
//得到字符属于哪一个状态组
int belong_v(char a,vector<vector<char>>A)
{
	for (int i = 0; i <A.size(); i++)
	{
		for (int j = 0; j < A[i].size(); j++)
		{
			if (a==A[i][j])
			{
				return i;
			}
		}
	}
	return -1;
}
//判断向量是否被包含于另一个向量
int belong_v(vector<char> a, vector<char>A)
{
	int m_count = 0;
	for (int i = 0; i < a.size(); i++)
	{
		for (int j = 0; j < A.size(); j++)
		{
			if (a[i]==A[j])
			{
				m_count++;
			}
		}
	}
	if (m_count==a.size())
	{
		return 1;
	}
	else
	{
		return -1;
	}
	
}


//分割开始和结束状态
void split_v(vector<DFA> target, vector<char> m_start, vector<char> m_accept,vector<vector<char>>& result )
{
	vector<vector<char>> res_start;
	res_start.push_back(m_start);
	res_start.push_back(m_accept);
	int flag = 0;
	while (true)
	{
		flag = res_start.size();
		vector<vector<char>> res_temp=res_start;
		for (int i = 0; i < res_start.size(); i++)
		{
			if (res_start[i].size() == 1)
			{
				continue;
			}
			else {
				for (int j = 0; j < res_start[i].size(); j++)
				{
					if (is_in(find_a_tag(res_start[i][j], target), res_start[i]) && is_in(find_b_tag(res_start[i][j], target), res_start[i]))
					{
						continue;
					}
					else
					{
						vector<char> temp;
						temp.push_back(res_start[i][j]);
						for (vector<char>::iterator iter = res_temp[i].begin(); iter != res_temp[i].end(); iter++)
						{        
							if (*iter == res_temp[i][j]) {
								res_temp[i].erase(iter);
								break;
							}
						}
						res_temp.push_back(temp);
						break;
					}
				}
			}
		}
		res_start = res_temp;
		if (res_start.size()==flag)
		{
			break;
		}
	}
	result = res_start;

}
//链接各个分割后的状态，组合成状态组
void connect_v(vector<DFA> target, vector<vector<char>>& result, vector<char> m_start,vector<char> m_accept)
{
	vector<vector<char>> res_start;
	res_start = result;
	int flag = 0;
	while (true)
	{
		flag = res_start.size();
		vector<vector<char>> res_temp = res_start;
		for (int i = 0; i < res_start.size()-1; i++)
		{
				for (int j = i+1; j < res_start.size(); j++)
				{
					if (belong_v(find_va_tag(res_start[i],target),res_start)== belong_v(find_va_tag(res_start[j], target), res_start)&&
						belong_v(find_vb_tag(res_start[i], target), res_start) == belong_v(find_vb_tag(res_start[j], target), res_start))
					{
						if (belong_v(find_va_tag(res_start[i], target), res_start)==-1|| belong_v(find_vb_tag(res_start[i], target), res_start)==-1)
						{
							continue;
						}
						else
						{
							if (belong_v(res_start[i],m_start)== belong_v(res_start[j], m_start)|| belong_v(res_start[i],m_accept) == belong_v(res_start[j], m_accept))
							{
								vector<char>temp = res_temp[j];
								for (vector<vector<char>>::iterator iter = res_temp.begin(); iter != res_temp.end(); iter++)
								{
									if (*iter == res_temp[j]) {
										res_temp.erase(iter);
										break;
									}
								}
								for (int k = 0; k < temp.size(); k++)
								{
									res_temp[i].push_back(temp[k]);
								}
								break;
							}
							else
							{

								continue;
							
							}
						}
					}
				}
				break;
		}
		res_start = res_temp;
		if (res_start.size() == flag)
		{
			break;
		}
	}
	result = res_start;
}
//写操作
void OutputFile(vector<Res>& v_tuple, string file, vector<int> a)
{
	ofstream on(file);
	for (int i = 0; i < v_tuple.size(); i++)
	{
		on << v_tuple[i] << endl;
	}
	on << "start state:";
	for (int i = 0; i < a.size(); i++)
	{
		if (a[i] == 0)
		{
			on <<i << ",";
		}
	}
	on << endl;
	on << "accepting states:";
	for (int i = 0; i < a.size(); i++)
	{
		if (a[i] == 1)
		{
			on << i << ",";
		}
	}
	on << endl;

	on.close();
}
//创建三元组
void create_tuple(vector<DFA> target,vector<vector<char>> result,vector<Res>& res)
{
	Res temp;
	for (int i = 0; i < result.size(); i++)
	{
		temp.a = i;
		temp.c = belong_v(find_va_tag(result[i],target),result);
		temp.b = 'a';
		res.push_back(temp);
	}
	for (int i = 0; i < result.size(); i++)
	{
		temp.a = i;
		temp.c = belong_v(find_vb_tag(result[i], target), result);
		temp.b = 'b';
		res.push_back(temp);
	}
}
//判断个状态组是属于起始状态还是接受状态
void findstate(vector<vector<char>>& res, vector<char> m_accept, vector<int>& a)
{
	for (int i = 0; i < res.size(); i++)
	{
		int flag = 0;
		for (int j = 0; j < m_accept.size(); j++)
		{
			if (is_in(m_accept[j],res[i]))
			{
				if (flag==0)
				{
					a.push_back(1);
				}
				
				flag = 1;
			}
		}
		if (flag==0)
		{
			a.push_back(0);
		}
	}
}

int main()
{
	vector<DFA> target; vector<char> m_start; vector<char> m_accept;
	vector<vector<char>> result;
	vector<Res> res;
	vector<int> x;
	ReadFile("input.txt", target, m_start, m_accept);
	split_v(target, m_start, m_accept, result);
	connect_v(target, result,m_start,m_accept);
	//调试代码
	/*for (int i = 0; i < result.size(); i++)
	{
		for (int j = 0; j < result[i].size(); j++)
		{
			cout << result[i][j] << " ";
		}
		cout << endl;
	}*/
	create_tuple(target, result, res);
	/*for (int i = 0; i < res.size(); i++)
	{
		cout << res[i].a << " " << res[i].b << " " << res[i].c<<endl;
	}*/
	findstate(result, m_accept, x);
	OutputFile(res, "output.txt", x);

}
