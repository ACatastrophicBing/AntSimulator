#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include <list>
#include <random>
#include "ant.hpp"
#include "utils.hpp"
#include "world.hpp"
#include <cmath>


struct Colony
{
  /**
   * @brief Construct a new Colony object
   * 
   * @param x Colony X position
   * @param y Colony Y position
   * @param n Colony Number of ants
   * @param mal_prob_food Probability of an ant being malicious placing down false food (fraction of ants being malicious)
   * @param mal_prob_home Probability of an ant being malicious placing down false home (fraction of ants being malicious)
   * @param mal_timer_delay Delay after which the attack is launched
   * @param malicious_ants_focus  Should the attack be focused towards food
   * @param ant_tracing_pattern   Should malicious ants trace food pheromone or roam randomly
	 * @param counter_pheromone Will the ants secret counter pheromone?
	 * @param hell_phermn_intensity_multiplier multiplier for the intensity of TO_HELL pheromone
   */
	Colony(float x, float y, uint32_t n, float mal_prob_food, float mal_prob_home, int mal_timer_delay, bool malicious_ants_focus = true, 
          AntTracingPattern ant_tracing_pattern = AntTracingPattern::RANDOM, bool counter_pheromone = false,
          float hell_phermn_intensity_multiplier = 1.0, bool uniform = false, bool concentrated = false, float concentrated_radius = 0, float concentrated_x = 0, float concentrated_y = 0 )
		: position(x, y)
		, last_direction_update(0.0f)
		, ants_va(sf::Quads, 4 * n)
    , mal_timer_delay(mal_timer_delay)
    , timer_count(0)
    , timer_count2(0)
    , confused_count(0)
	{
    // std::cout<<std::abs(((double) rand() / (RAND_MAX)));
      // std::cout<<"Normal";

    for (uint64_t i(0); i < n; ++i) {
      if(i >= (mal_prob_home + mal_prob_food)*n)
      {
        ants.emplace_back(x, y, getRandRange(2.0f * PI), counter_pheromone);

        const uint64_t index = 4 * i;
        ants_va[index + 0].color = Conf::ANT_COLOR;
        ants_va[index + 1].color = Conf::ANT_COLOR;
        ants_va[index + 2].color = Conf::ANT_COLOR;
        ants_va[index + 3].color = Conf::ANT_COLOR;

        ants_va[index + 0].texCoords = sf::Vector2f(0.0f, 0.0f);
        ants_va[index + 1].texCoords = sf::Vector2f(73.0f, 0.0f);
        ants_va[index + 2].texCoords = sf::Vector2f(73.0f, 107.0f);
        ants_va[index + 3].texCoords = sf::Vector2f(0.0f, 107.0f);
      }
      else
      {
          // STARTING ANGLE OF MALICIOUS ANT
          float angle;
          if(malicious_ants_focus)
            angle = -3*PI/4;
          else
            angle = getRandRange(2.0f * PI); // Sets even distribution
          

          /* Placement of Malicious ants */
          float x_malicious = x;
          float y_malicious = y;
          bool is_Valid = false;
          if(uniform){ /* TOFO : add something to the config file to select a placement scheme*/
            std::random_device rd;  // Will be used to obtain a seed for the random number engine
            std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
            std::uniform_real_distribution<> disx(0.0, Conf::WIN_WIDTH);
            std::uniform_real_distribution<> disy(0.0, Conf::WIN_HEIGHT);
            x_malicious = (float)disx(gen);
            y_malicious = (float)disy(gen);
          }

          if(concentrated){ // TODO : Also add UNIFORM, UNIFORM_RADIUS, MAL_HOME_X, MAL_HOME_Y, TARGETED
            if(concentrated_x == 0 || concentrated_y == 0){
              x_malicious = x;
              y_malicious = y;
            } else {
              x_malicious = concentrated_x * Conf::WIN_WIDTH;
              y_malicious = concentrated_y * Conf::WIN_HEIGHT;
            }
            if(uniform){
              std::random_device rd;  // Will be used to obtain a seed for the random number engine
              std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
              std::uniform_real_distribution<> disr(0.0, x + concentrated_radius);
              std::uniform_real_distribution<> disrad(0.0, 3.14159);
              // TODO : find the vector location of the above
              float direction = disrad(gen);
              x_malicious = x_malicious + concentrated_radius * cos(direction);
              y_malicious = y_malicious + concentrated_radius * sin(direction);
            }
          }
            
          if(i <= mal_prob_food*n) {// Place malicious food ant
            ants.emplace_back(x_malicious, y_malicious, angle, false, true, false, ant_tracing_pattern, hell_phermn_intensity_multiplier); 
          }
          else if(i <= (mal_prob_home + mal_prob_food)*n) {// Place malicious home ant
            ants.emplace_back(x_malicious, y_malicious, angle, false, false, true, ant_tracing_pattern, hell_phermn_intensity_multiplier);
          } 

          const uint64_t index = 4 * i;
          ants_va[index + 0].color = Conf::MALICIOUS_ANT_COLOR;
          ants_va[index + 1].color = Conf::MALICIOUS_ANT_COLOR;
          ants_va[index + 2].color = Conf::MALICIOUS_ANT_COLOR;
          ants_va[index + 3].color = Conf::MALICIOUS_ANT_COLOR;

          ants_va[index + 0].texCoords = sf::Vector2f(0.0f, 0.0f);
          ants_va[index + 1].texCoords = sf::Vector2f(73.0f, 0.0f);
          ants_va[index + 2].texCoords = sf::Vector2f(73.0f, 107.0f);
          ants_va[index + 3].texCoords = sf::Vector2f(0.0f, 107.0f);
		  }
    }
	}

	void update(const float dt, World& world)
	{	
    confused_count = 0;
    ants_that_found_food = 0; 
    ants_that_delivered_food = 0;
    bool wreak_havoc = timer_count >= mal_timer_delay ? true : false;
		for (Ant& ant : ants) {
      if(!skip_once)
			  ant.checkColony(position);
			ant.update(dt, world, wreak_havoc);
      if(ant.didAntFindFood())
        ants_that_found_food++;
      if(ant.didAntDeliverFood())
        ants_that_delivered_food++;
		}
    skip_once = false;
    if(wreak_havoc)
    {
      timer_count = 0;
    }
    else
      timer_count ++;
    timer_count2 ++;
	}

  static int getAntsThatFoundFood()
  {
    return ants_that_found_food;
  }

  static int getAntsThatDeliveredFood()
  {
    return ants_that_delivered_food;
  }

	void render(sf::RenderTarget& target, const sf::RenderStates& states) const
	{
		for (const Ant& a : ants) {
			a.render_food(target, states);
		}

		uint32_t index = 0;
		for (const Ant& a : ants) {
			a.render_in(ants_va, 4 * (index++));
		}

		sf::RenderStates rs = states;
		rs.texture = &(*Conf::ANT_TEXTURE);
		target.draw(ants_va, rs);
	}

	const sf::Vector2f position;
	std::vector<Ant> ants;
	mutable sf::VertexArray ants_va;
	const float size = 20.0f;

	float last_direction_update;
	const float direction_update_period = 0.25f;

  int mal_timer_delay;
  int timer_count;
  int timer_count2;
  int confused_count;
  float counter_rise_fraction;
  bool skip_once = true;

  inline static int ants_that_found_food;
  inline static int ants_that_delivered_food;
};
