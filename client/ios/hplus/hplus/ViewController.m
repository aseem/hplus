//
//  ViewController.m
//  hplus
//
//  Created by aseem on 10/31/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import "ViewController.h"
#import "HPServiceManager.h"
#import "HPServiceManagerDelegate.h"
#import "HPServiceCommunicator.h"

@interface ViewController () <HPServiceManagerDelegate>
{
    NSArray *_groups;
    HPServiceManager *_manager;
}
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    _manager = [[HPServiceManager alloc] init];
    _manager.communicator = [[HPServiceCommunicator alloc] init];
    _manager.communicator.delegate = _manager;
    _manager.delegate = self;
    
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


#pragma mark - View Actions
- (IBAction)getStories:(id)sender
{
    [_manager fetchStories];
}

#pragma mark - HPServiceManagerDelegate

- (void) didReceiveStories:(NSArray *)stories
{
    NSLog(@"Stories:");
    NSLog(@"%@", stories);
}

- (void) fetchingStoriesFailedWithError:(NSError *)error
{
    NSLog(@"Failed to retreive stories - Error: %@; %@", error, [error localizedDescription]);
}


@end
