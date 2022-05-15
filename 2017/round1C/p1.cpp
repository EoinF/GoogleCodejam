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

long double solve_case(CaseParams params);

struct Pancake
{
    int r;
    int h;
    long double side_area;
    long double top_area;

    Pancake(int r, int h)
    {
        this->r = r;
        this->h = h;
        this->side_area = 2.0l * M_PI * r * h;
        this->top_area = M_PI * r * r;
    }
};

void solve_problem()
{
    int test_cases = read_int();

    CaseParams params;
    for (int c = 1; c < test_cases + 1; c++)
    {
        params.read_params();
        cout << "Case #" << c << ": " << fixed << setprecision(20) << solve_case(params) << endl;
    }
}

long double get_best_k_minus_1(vector<Pancake> pancakes, int index, int max_k, vector<vector<long double>> cache)
{
    if (max_k == 0)
    {
        cache[index][0] = 0;
        return 0;
    }
    if (cache[index][max_k] == -1)
    {
        long double best_area = 0;
        for (int i = index + 1; i < 2 + pancakes.size() - max_k; i++)
        {
            long double new_area = pancakes[index].side_area + get_best_k_minus_1(pancakes, i, max_k - 1, cache);
            best_area = max(new_area, best_area);
        }
        cache[index][max_k] = best_area;
    }

    return cache[index][max_k];
}

long double solve_case(CaseParams params)
{
    vector<Pancake> pancakes;
    for (int i = 0; i < params.n; i++)
    {
        int r = read_int();
        int h = read_int();
        pancakes.push_back(Pancake(r, h));
    }

    sort(pancakes.begin(), pancakes.end(),
         [](Pancake p1, Pancake p2)
         {
             return p1.r > p2.r;
         });

    vector<vector<long double>> cache;
    cache.resize(params.n + 1);
    for (auto &c : cache)
    {
        c.resize(params.k + 1, -1);
    }

    long double best_area = 0;
    long double current_area;

    if (params.k == params.n)
    {
        best_area += pancakes[0].top_area;
        for (auto p : pancakes)
        {
            best_area += p.side_area;
        }
        return best_area;
    }
    for (int index = 0; index < 1 + params.n - params.k; index++)
    {
        auto p = pancakes[index];
        // solve best k for p
        cache[index][params.k] = get_best_k_minus_1(pancakes, index, params.k, cache);

        current_area = p.top_area + cache[index][params.k];
        best_area = max(best_area, current_area);
    }

    return best_area;
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    solve_problem();
}
