#include<iostream>
#include<fstream>
#include<vector>
#include<iomanip>
#include<string>
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



//写操作
void OutputFile(vector<MYT>& v_tuple, string file)
{
	ofstream on(file,ios::app);
	for (int i = 0; i < v_tuple.size(); i++)
	{
		on << v_tuple[i] << endl;
	}
	on << "start state : 0"<<endl;
	on <<"accepting states: "<<v_tuple[v_tuple.size()-1].end<<endl;
	on << endl;
	on.close();
}
//将指定位置向量向后移动一位
void changeresult(vector<MYT>& temp, int begin, int end)
{
	for (int i = temp.size() - 1; i >= 0; i--)
	{
		if (temp[i].beg >= begin && temp[i].end <= end)
		{
			temp[i].beg++;
			temp[i].end++;
		}
		else
		{
			break;
		}
	}
}
//创建三元组并且进行对应特殊字符的指定操作
int* createtuple(vector<MYT>& result, string target, int beg = 0, int end = 1)
{
	int flag = 0;
	int flag_r = 0;
	int or_beg = beg;
	int t_beg = beg;
	int t_end = end;
	int flag_tap = 0;
	int r_tap = 0;
	int i = 0;
	int p[3];
	int* r = 0;
	do
	{
		char temp = target[i];
		if (temp == '*')//前后拼接一个节点
		{
			if (target[i - 1] == ')')
			{
				int tap = r_tap;
				MYT t1(tap, 'e', tap + 1);
				MYT t3(t_end, 'e', t_end + 1);
				MYT t4(t_end, 'e', tap + 1);
				MYT t5(tap, 'e', t_end + 1);
				changeresult(result, tap, t_end - 1);
				result.push_back(t1);
				result.push_back(t3);
				result.push_back(t4);
				result.push_back(t5);
				t_beg = t_end + 1;
				t_end = t_end + 2;
			}
			else
			{
				result.pop_back();
				MYT t1(t_beg - 1, 'e', t_beg);
				MYT t2(t_beg, target[i - 1], t_end);
				MYT t3(t_end, 'e', t_end + 1);
				MYT t4(t_end, 'e', t_beg);
				MYT t5(t_beg - 1, 'e', t_end + 1);
				result.push_back(t1);
				result.push_back(t2);
				result.push_back(t3);
				result.push_back(t4);
				result.push_back(t5);
				t_beg = t_end + 2;
				t_end = t_end + 3;
			}
		}
		else if (temp == '|')//先完成前半部分的前节点扩充
		{
			if (target[i - 1] == ')')
			{
				int tap = r_tap;
				MYT t1(tap, 'e', tap + 1);
				changeresult(result, tap, t_end - 1);
				result.push_back(t1);
				flag_tap = tap;
				t_beg = t_end;
				t_end = t_end + 1;
				flag = 1;
				if (target[i + 1] == '(')
				{
					flag_r = 1;
				}
			}
			else
			{
				result.pop_back();
				MYT t1(t_beg - 1, 'e', t_beg);
				MYT t2(t_beg, target[i - 1], t_end);
				result.push_back(t1);
				result.push_back(t2);
				flag_tap = t_beg - 1;
				t_beg = t_end;
				t_end = t_end + 1;
				flag = 1;
				if (target[i + 1] == '(')
				{
					flag_r = 1;
				}
			}


		}
		else if (temp == '(')//递归完成返回
		{
			string new_target(target, i + 1);
			r = createtuple(result, new_target, t_beg, t_end);
			i = i + *(r + 1) + 1;
			t_beg = *(r + 2) - 1;
			t_end = *(r + 2);
			r_tap = *r;
		}
		else if (temp == ')')
		{
			p[0] = or_beg;
			p[1] = i;
			p[2] = t_end;
			return p;
		}
		else if (flag > 0)//完成|后半部分的扩展已经上半部分的节点补充
		{
			if (flag_r == 0)
			{

				MYT t1(flag_tap, 'e', t_end);
				MYT t2(t_end, temp, t_end + 1);
				MYT t3(t_end + 1, 'e', t_end + 2);
				MYT t4(t_beg, 'e', t_end + 2);
				result.push_back(t1);
				result.push_back(t2);
				result.push_back(t3);
				result.push_back(t4);
				flag = 0;
				t_beg = t_end + 2;
				t_end = t_end + 3;
			}
			else
			{
				int tap = r_tap;
				MYT t1(flag_tap, 'e', tap + 1);
				MYT t3(t_end, 'e', t_end + 1);
				MYT t4(tap, 'e', t_end + 1);
				changeresult(result, tap, t_end - 1);
				result.push_back(t1);
				result.push_back(t3);
				result.push_back(t4);
				flag = 0;
				flag_r = 0;
				t_beg = t_end + 1;
				t_end = t_end + 2;
			}
		}
		else
		{
			MYT t(t_beg, temp, t_end);
			result.push_back(t);
			t_beg++;
			t_end++;
		}
		i++;
	} while (i < target.size() || flag_r == 1);
}
//读操作并且调用创建三元组函数同步生成
int ReadFile_doMYT(string file)
{
	ifstream in(file);
	string temp;
	if (!in)
	{
		cout << "wrong" << endl;
		return -1;
	}
	ofstream on("output.txt");
	on << endl;
	on.close();
	while (in >> temp)
	{
		vector<MYT> result;
		createtuple(result, temp);
		OutputFile(result, "output.txt");
	}
	return 1;
}

int main()
{
	ReadFile_doMYT("input.txt");
}