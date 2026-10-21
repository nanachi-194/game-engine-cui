#include <iostream>
#include <fstream>
#include <algorithm>
#include <cstdlib>
#include <cwchar>
#include "linux_conio.h"
#include "windows.h"

constexpr int MAP_WIDTH = 10;
constexpr int MAP_HEIGHT = 5;
constexpr int MAP_LIST_X = 3;
constexpr int MAP_LIST_Y = 3;
constexpr int MAP_LIST_SIZE = 2;

void printMap(int map[MAP_LIST_SIZE][MAP_LIST_Y][MAP_LIST_X][MAP_HEIGHT][MAP_WIDTH], int map_list_size, bool key_3, bool key_5 , int map_player_x, int map_player_y, int player_x, int player_y, bool player_win){
    std::cout << "\033[2J\033[H" << std::flush;
    if (player_win == true){
        std::cout << "\033[34mplayer\033[0m win\n";
    }
    else{
        for (int y = 0; y < MAP_HEIGHT; y++) {

            for (int x = 0; x < MAP_WIDTH; x++) {
                if (x == player_x && y == player_y) {
                    std::cout << "\033[34mp\033[0m";
                }
                else {
                    if (map[map_list_size][map_player_y][map_player_x][y][x] == 1) {
                        std::cout << "\033[46m1\033[0m";
                    }else if(map[map_list_size][map_player_y][map_player_x][y][x] == 2){
                        std::cout << "\033[31m2\033[0m";
                    }else if(map[map_list_size][map_player_y][map_player_x][y][x] == 3){
                        if (key_3 == true) {
                            std::cout << "0";
                        }else{
                            std::cout << "\033[43m3\033[0m";
                        }
                    }else if(map[map_list_size][map_player_y][map_player_x][y][x] == 4){
                        std::cout << "\033[43m4\033[0m";
                    }else if(map[map_list_size][map_player_y][map_player_x][y][x] == 5){
                        if (key_5 == true) {
                            std::cout << "0";
                        }else{
                            std::cout << "\033[45m5\033[0m";
                        }
                    }else if(map[map_list_size][map_player_y][map_player_x][y][x] == 6){
                        std::cout << "\033[45m6\033[0m";
                    }else if(map[map_list_size][map_player_y][map_player_x][y][x] == 7){
                        std::cout << "\033[31m7\033[0m";
                    }else if(map[map_list_size][map_player_y][map_player_x][y][x] == 0){
                        std::cout << "0";
                    }
                }
            }
        std::cout << "\n";
        }
        std::cout << "\033[34mPlayer1\033[0m : x(" << player_x
                << ") y(" << player_y << ") win(" << player_win 
                << ") key_3(" << key_3 << ") key_5(" << key_5 << ")\n";

            #ifdef _WIN32
            std::cout << "You PC is Windows PC. \n\n" ;
            #elif defined(__linux__)
            std::cout << "You PC is Linux PC. \n\n";
            #endif
    }
}

int main(){

    enable_conio_mode();
    #ifdef _WIN32
    std::system("cls");
    #elif defined(__linux__)
    std::system("clear");
    #endif

    int player_x = 0;
    int player_y = 1;
    int map_player_x = 0;
    int map_player_y = 0;
    bool player_win = false;

    int map_list_size = 0;

    bool key_3 = false;
    bool key_5 = false;

    bool door_4 = false;
    bool door_6 = false;

    int map[MAP_LIST_SIZE][MAP_LIST_Y][MAP_LIST_X][MAP_HEIGHT][MAP_WIDTH];

    std::ifstream map_date("map.map");

    if (!map_date) {
        std::cout << "Not map.map file.\n";
        return 1;
    }

    for (int size = 0; size < MAP_LIST_SIZE; size++) {
        for (int y = 0; y < MAP_LIST_Y; y++) {
            for (int x = 0; x < MAP_LIST_X; x++) {
                for (int height = 0; height < MAP_HEIGHT; height++) {
                    for (int width = 0; width < MAP_WIDTH; width++) {
                        map_date >> map[size][y][x][height][width];
                    }
                }
            }
        }
    }

    printMap(map, map_list_size, key_3, key_5, map_player_x, map_player_y, player_x, player_y, player_win);

    while (true) {

        if (_kbhit()) {
            if (key_3 == true){
                door_4 = true;
            }
            if (key_5 == true){
                door_6 = true;
            }

            int key = _getch();

            if (key == 'w') {

                int next_x = player_x;
                int next_y = player_y - 1;

                int next_map_player_x = map_player_x;
                int next_map_player_y = map_player_y;

                if (next_y < 0) {

                    if (next_map_player_y > 0) {
                        next_map_player_y--;
                        next_y = MAP_HEIGHT - 1;
                    }
                }

                int tile = map[map_list_size][next_map_player_y][next_map_player_x][next_y][next_x];

                bool canMove = false;

                if (tile == 0) {
                    canMove = true;
                }
                else if (tile == 2) {
                    canMove = true;
                }
                else if (tile == 3) {
                    canMove = true;
                }
                else if (tile == 5) {
                    canMove = true;
                }else if (tile == 7) {
                    canMove = true;
                }
                else if (tile == 7) {
                    canMove = true;
                }
                else if (tile == 4 && door_4 == true) {
                    canMove = true;
                }
                else if (tile == 6 && door_6 == true) {
                    canMove = true;
                }

                if (canMove) {
                    player_x = next_x;
                    player_y = next_y;

                    map_player_x = next_map_player_x;
                    map_player_y = next_map_player_y;
                }

                if (map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 2) {
                    player_win = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 3) {
                    key_3 = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 5) {
                    key_5 = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 7) {
                    map_list_size += 1;
                    player_x = 0;
                    player_y = 1;
                    map_player_x = 0;
                    map_player_y = 0;

                    key_3 = false;
                    key_5 = false;

                    door_4 = false;
                    door_6 = false;
                }
            }


            else if (key == 's') {

                int next_x = player_x;
                int next_y = player_y + 1;

                int next_map_player_x = map_player_x;
                int next_map_player_y = map_player_y;

                if (next_y >= MAP_HEIGHT) {

                        if (next_map_player_y < MAP_LIST_Y - 1) {
                            next_map_player_y++;
                            next_y = 0;
                        }
                }

                int tile = map[map_list_size][next_map_player_y][next_map_player_x][next_y][next_x];

                bool canMove = false;

                if (tile == 0) {
                    canMove = true;
                }
                else if (tile == 2) {
                    canMove = true;
                }
                else if (tile == 3) {
                    canMove = true;
                }
                else if (tile == 5) {
                    canMove = true;
                }else if (tile == 7) {
                    canMove = true;
                }
                else if (tile == 4 && door_4 == true) {
                    canMove = true;
                }
                else if (tile == 6 && door_6 == true) {
                    canMove = true;
                }

                if (canMove) {
                    player_x = next_x;
                    player_y = next_y;

                    map_player_x = next_map_player_x;
                    map_player_y = next_map_player_y;
                }

                if (map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 2) {
                    player_win = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 3) {
                    key_3 = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 5) {
                    key_5 = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 7) {
                    map_list_size += 1;
                    player_x = 0;
                    player_y = 1;
                    map_player_x = 0;
                    map_player_y = 0;

                    key_3 = false;
                    key_5 = false;

                    door_4 = false;
                    door_6 = false;
                }
            }


            else if (key == 'a') {

                int next_x = player_x - 1;
                int next_y = player_y;

                int next_map_player_x = map_player_x;
                int next_map_player_y = map_player_y;

                if (next_x < 0) {

                    if (next_map_player_x > 0) {
                        next_map_player_x--;
                        next_x = MAP_WIDTH - 1;
                    }
                }

                int tile = map[map_list_size][next_map_player_y][next_map_player_x][next_y][next_x];

                bool canMove = false;

                if (tile == 0) {
                    canMove = true;
                }
                else if (tile == 2) {
                    canMove = true;
                }
                else if (tile == 3) {
                    canMove = true;
                }
                else if (tile == 5) {
                    canMove = true;
                }else if (tile == 7) {
                    canMove = true;
                }
                else if (tile == 4 && door_4 == true) {
                    canMove = true;
                }
                else if (tile == 6 && door_6 == true) {
                    canMove = true;
                }

                if (canMove) {
                    player_x = next_x;
                    player_y = next_y;

                    map_player_x = next_map_player_x;
                    map_player_y = next_map_player_y;
                }

                if (map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 2) {
                    player_win = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 3) {
                    key_3 = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 5) {
                    key_5 = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 7) {
                    map_list_size += 1;
                    player_x = 0;
                    player_y = 1;
                    map_player_x = 0;
                    map_player_y = 0;

                    key_3 = false;
                    key_5 = false;

                    door_4 = false;
                    door_6 = false;
                }
            }


            else if (key == 'd') {

                int next_x = player_x + 1;
                int next_y = player_y;

                int next_map_player_x = map_player_x;
                int next_map_player_y = map_player_y;

                if (next_x >= MAP_WIDTH) {

                    if (next_map_player_x < MAP_LIST_X - 1) {
                        next_map_player_x++;
                        next_x = 0;
                    }
                }

                int tile = map[map_list_size][next_map_player_y][next_map_player_x][next_y][next_x];

                bool canMove = false;

                if (tile == 0) {
                    canMove = true;
                }
                else if (tile == 2) {
                    canMove = true;
                }
                else if (tile == 3) {
                    canMove = true;
                }
                else if (tile == 5) {
                    canMove = true;
                }else if (tile == 7) {
                    canMove = true;
                }
                else if (tile == 4 && door_4 == true) {
                    canMove = true;
                }
                else if (tile == 6 && door_6 == true) {
                    canMove = true;
                }

                if (canMove) {
                    player_x = next_x;
                    player_y = next_y;

                    map_player_x = next_map_player_x;
                    map_player_y = next_map_player_y;
                }
                
                if (map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 2) {
                    player_win = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 3) {
                    key_3 = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 5) {
                    key_5 = true;
                }else if(map[map_list_size][map_player_y][map_player_x][player_y][player_x] == 7) {
                    map_list_size += 1;
                    player_x = 0;
                    player_y = 1;
                    map_player_x = 0;
                    map_player_y = 0;

                    key_3 = false;
                    key_5 = false;

                    door_4 = false;
                    door_6 = false;
                }
            }

            else if (key == 'q') {
                break;
            }
            else {
                continue;
            }

            player_x = std::clamp(player_x, 0, MAP_WIDTH - 1);
            player_y = std::clamp(player_y, 0, MAP_HEIGHT - 1);
            map_player_x = std::clamp(map_player_x, 0, MAP_LIST_X - 1);
            map_player_y = std::clamp(map_player_y, 0, MAP_LIST_Y - 1);

            printMap(map, map_list_size, key_3, key_5, map_player_x, map_player_y, player_x, player_y, player_win);
        }
    }
    disable_conio_mode();

    return 0;
}
