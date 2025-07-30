
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>

std::vector<std::vector<float>> CSVRead(std::string file_name){
     std::vector<std::vector<float>> csv_data;

     std::vector<float> row_data;
     std::string line, data;

     std::fstream file (file_name, std::ios::in);
	if(file.is_open()){
		while(getline(file, line)){
			row_data.clear();
               std::stringstream str(line);

			while(getline(str, data, ',')){
                    float data_point = std::stof(data);
                    row_data.push_back(data_point);
               }
			csv_data.push_back(row_data);
		}
	}
	else printf("%s", "Could not open the file\n");
 
     return csv_data;
}

