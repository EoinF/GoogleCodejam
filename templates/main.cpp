#include <bits/stdc++.h>
using namespace std;

#define M_PI 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679

int read_int()
{
    int x;
    cin >> x;
    return x;
}

vector<int> read_ints(int n)
{
    int val;
    vector<int> values;
    for (int i = 0; i < n; i++)
    {
        cin >> val;
        values.push_back(val);
    }
    return values;
}

vector<string> read_strings(int n)
{
    string val;
    vector<string> values;
    for (int i = 0; i < n; i++)
    {
        cin >> val;
        values.push_back(val);
    }
    return values;
}

struct CaseParams
{
    int n;
    int k;

    void read_params()
    {
        this->n = read_int();
        this->k = read_int();
    }
};

string solve_case(CaseParams params)
{
}

void solve_problem()
{
    int test_cases = read_int();

    CaseParams params;
    for (int c = 1; c < test_cases + 1; c++)
    {
        params.read_params();
        cout << "Case #" << c << ": " << solve_case(params) << endl;
    }
}
int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    solve_problem();
}
